import pymysql
from .models import Passage
from bosonnlp import BosonNLP

# 获取热点关键词列表
def get_key_word_list(num):
    conn = pymysql.connect(host='127.0.0.1',  user='admin', passwd='Ryan', db="omdb",charset='UTF8')
    cur = conn.cursor()

    sql_str = r"select keyword_id , count(*) AS count, passage_id from opinionmonitor_passage_keywords group by keyword_id order by count DESC limit 0,{0};".format(num)
    cur.execute(sql_str)
    key_id_list = []
    key_id_set = set()
    for ii in cur:
        key_id_list.append([ii[0], ii[1]])
        key_id_set.add(ii[0])

    result_list = []
    for key_id, c_num in key_id_list:
        sql_str = "select word from opinionmonitor_keyword where kid={0};".format(key_id)
        cur.execute(sql_str)
        for ii in cur:
            result_list.append([ii[0], c_num])
    return result_list


def get_focus_passage(num):
    pass


def get_search_result(keyword, page, num=10):
    result_list = []
    page_list = []
    n_page = page
    p_page = page
    num_page = 0
    if keyword == "%敏感文章%":
        # 计算总页数
        num_page = len(Passage.objects.filter(st__lte=1, forbiddenNum__gte=10).order_by('st')) / num
        result_list.extend(
            Passage.objects.filter(st__lte=1, forbiddenNum__gte=10).order_by('st')[num * page:num * (page + 1)])

    elif keyword == "%舆情热点%":
        num_page = len(Passage.objects.order_by('c_read')[0:20])
        result_list.extend(Passage.objects.order_by('c_read')[0:20])
    else:
        while "  " in keyword:
            keyword = keyword.replace("  ", " ")
        keyword_list = keyword.split(" ")
        tmp_passage = None
        for key in keyword_list:
            if tmp_passage:
                tmp_passage = tmp_passage.filter(content__contains=key)
            else:
                tmp_passage = Passage.objects.filter(content__contains=key)
        num_page = len(tmp_passage)/ num
        result_list.extend(tmp_passage[num * page:num * (page + 1)])

    if num_page % 10 > 0:
        num_page = int(num_page) + 1
    else:
        num_page = int(num_page)

    # 计算上一页
    if p_page - 1 < 0:
        p_page = 0
    else:
        p_page -= 1

    # 计算下一页
    if n_page + 1 > num_page:
        n_page = num_page
    else:
        n_page += 1

    for i in range(1, num_page + 1):
        page_list.append(i)

    # 提取简要用于显示
    for result in result_list:
        if keyword == ("%敏感文章%" or "%舆情热点%"):
            result.content = result.get_abstract()
        else:
            result.content = result.get_abstract(keyword)
        result.st = round(result.st*100, 1)

    context = {
        'result_list': result_list,
        'current_page': page,
        'p_page': p_page,
        'n_page': n_page,
        "page_list": page_list,
        'num_page': num_page,
        "keyword": keyword,
    }

    return context

from gensim import similarities
from collections import OrderedDict
def get_similar_text(text):
    BosonNLPKey = "BMRivntt.8194.5zwvLwj_ygkV"
    # ZfXxO6kv.10841.LZ_TDcJiiwrl
    nlp = BosonNLP(BosonNLPKey)

    # 获取关键词 [[0.8391345017584958, '病毒式'], [0.3802418301341705, '蔓延']]
    keyword_result = nlp.extract_keywords(text, top_k=10)
    print(keyword_result)
    # keyword_result = [[0.36443758441765906, '卖艺'], [0.26732109821670036, '路学院'], [0.2667011448568187, '挣钱'], [0.23801264121689353, '天目山'], [0.22618147770853975, '走时'], [0.22553389408212396, '孩子'], [0.21006863070452944, '一老一少'], [0.18830464004379927, '儿子'], [0.18298766176875855, '育才'], [0.17494405471962107, '红绿灯']]
    key_word_list = []
    for key_item in keyword_result:
        if key_item[0] > 0.15 and len(key_item[1])<10:
            key_word_list.append((key_item[1],key_item[0]))

    conn = pymysql.connect(host='127.0.0.1',  user='admin', passwd='Ryan', db="omdb",charset='UTF8')
    cur = conn.cursor()
    vec_tfidf = []
    for key in key_word_list:
        sql_str = "SELECT kid from opinionmonitor_keyword WHERE word = '{0}'".format(key[0])
        cur.execute(sql_str)
        for ii in cur:
            vec_tfidf.append((ii[0], key[1]))

    pid_list = []
    for key_id in vec_tfidf:
        sql_str = "SELECT pid_id from opinionmonitor_passagekeyword WHERE kid_id = {0}".format(key_id[0])
        cur.execute(sql_str)
        for ii in cur:
            pid_list.append(ii[0])

    # 统计重复次数
    pid_set = set(pid_list)
    corpus_tfidf = []
    p_id_list = []
    for pid in pid_set:
        c = pid_list.count(pid)

        # 大于2才加入结果集中
        if c > 0:
            sql_str = "SELECT kid_id, ratio from opinionmonitor_passagekeyword WHERE pid_id = {0}".format(pid)
            cur.execute(sql_str)
            kr_list = []
            for ii in cur:
                kr_list.append((ii[0], ii[1]))
            corpus_tfidf.append(kr_list)
            p_id_list.append(pid)


    cur.close()                                    #关闭游标
    conn.commit()                                  #向数据库中提交任何未解决的事务，对不支持事务的数据库不进行任何操作
    conn.close()                                   #关闭到数据库的连接，释放数据库资源

    # 计算cos距离
    print("比较矩阵")
    print(corpus_tfidf)
    print("文本向量")
    print(vec_tfidf)
    if corpus_tfidf == []:
        return dict()
    index = similarities.MatrixSimilarity(corpus_tfidf)
    sims = index[vec_tfidf]

    r_pid_dict = dict()
    sim_result_list = list(sims)

    for index, item in enumerate(sim_result_list):
        if item > 0.5:
            r_pid_dict[p_id_list[index]] = item


    result_list = []
    result_order_dict = OrderedDict()
    r_pid_dict = OrderedDict(sorted(r_pid_dict.items(), key=lambda x: x[1]))
    print(r_pid_dict)
    for k, v in r_pid_dict.items():
        passage_list = Passage.objects.filter(pid=k)
        passage = passage_list[0]
        passage.st = v
        item_tuple = passage.to_tuple()
        result_order_dict[item_tuple[0]] = item_tuple[1]
        # result_list.append(passage.to_tuple())
    return result_order_dict