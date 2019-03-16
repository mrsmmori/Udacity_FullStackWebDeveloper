#!/usr/bin/env python
import psycopg2


def get_connection():
        return psycopg2.connect("dbname=news")


def get_question():
    with get_connection() as conn:
        with conn.cursor() as cur:

            # Question 1
            print "What are the most popular three articles of all time?"
            cur.execute('''
            select v_map.article_title, v_log.count from v_log join v_map on v_log.title = v_map.log_title order by count desc limit 3;
                        ''')
            articles = cur.fetchall()
            for article in articles:
                print "\t{}: {:,}".format(article[0], article[1])

            # Question 2
            print "Who are the most popular article authors of all time?"
            cur.execute('''
                        select v_authors.author, sum(v_log.count) from v_authors left join v_map on v_authors.title = v_map.article_title left join v_log on v_map.log_title = v_log.title group by v_authors.author order by sum desc limit 3;
                                    ''')
            authors = cur.fetchall()
            print "\t{}".format([i[0] for i in authors])

            # Question 3
            print "On which days did more than 1% of requests lead to errors?"
            cur.execute('''
            select day, round(cast(percentage as numeric) * 100, 2) from v_percentage where percentage > 0.01 order by percentage desc;
                                    ''')
            percentage = cur.fetchall()
            if percentage == []:
                print "\tNot applicable"
            else:
                for per in percentage:
                    print "\t{}: {}%".format(per[0], per[1])

get_question()
