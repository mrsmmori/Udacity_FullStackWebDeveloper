import psycopg2


def get_connection():
        return psycopg2.connect("dbname=news")


def get_question():
    with get_connection() as conn:
        with conn.cursor() as cur:

            # Question 1
            print "What are the most popular three articles of all time?"
            cur.execute('select map.article_title, v_log.count from v_log \
                        join map on v_log.title = map.log_title order \
                        by count desc;')
            articles = cur.fetchall()
            print "\t{}: {:,}".format(articles[0][0], articles[0][1])
            print "\t{}: {:,}".format(articles[1][0], articles[1][1])
            print "\t{}: {:,}".format(articles[2][0], articles[2][1])

            # Question 2
            print "Who are the most popular article authors of all time?"
            cur.execute('select v_authors.author, sum(v_log.count) \
                                    from v_authors \
                                    left join map on \
                                    v_authors.title = map.article_title \
                                    left join v_log on \
                                    map.log_title = v_log.title \
                                    group by v_authors.author \
                                    order by sum desc;')
            authors = cur.fetchall()
            print "\t{}: {:,}".format(authors[0][0], authors[0][1])

            # Question 3
            print "On which days did more than 1% of requests lead to errors?"
            cur.execute('select day, percentage \
                                    from v_percentage where percentage > 0.01 \
                                    order by percentage desc;')
            percentage = cur.fetchall()
            if percentage == []:
                print "\tNot applicable"
            else:
                for per in percentage:
                    print "\t{}: {:.2%}".format(per[0], per[1])

get_question()
