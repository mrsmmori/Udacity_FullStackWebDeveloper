
Log Analysis Program
====

# Overview
This program is written for Udacity / Full Stack Web Developer Nanodegree / Project 1.  
The objective of this practice project is to build an informative summary from logs that are stored in Postgresql server. 
3 question is provided:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Description
- **log_analysis.py** - written in python 2.7.12. This python code produce answers to above 3 questions.


## Setup

1. Run a Virtual machine (fsnd-virtual-machine)

``` bash
vagrant up
vagrant ssh
```

2. Download <a href="https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip">newsdata.zip</a>

3. To load data, cd into the vagrant directory and use the command.

```
psql -d news -f newsdata.sql
```

4. Setup below 4 view(s) in "news" database.

- v_map
```
create view v_map as
(
select 
'bad-things-gone' as log_title, 
'Bad things gone, say good people' as article_title
 union all 
select 
'balloon-goons-doomed' as log_title, 
'Balloon goons doomed' as article_title
 union all  
select 
'bears-love-berries' as log_title, 
'Bears love berries, alleges bear' as article_title
 union all 
select 
'candidate-is-jerk' as log_title, 
'Candidate is jerk, alleges rival' as article_title
 union all 
select 
'goats-eat-googles' as log_title, 
'Goats eat Google''s lawn' as article_title
 union all  
select 
'media-obsessed-with-bears' as log_title, 
'Media obsessed with bears' as article_title
 union all 
select 
'trouble-for-troubled' as log_title, 
'Trouble for troubled troublemakers' as article_title
 union all 
select 
'so-many-bears' as log_title, 
'There are a lot of bears' as article_title
);

```

- v_log  
```
create view v_log as 
select regexp_replace(path, '/article/' , '') as title, 
count(path) from log 
where status = '200 OK' and path != '/' 
group  by title;
```
- v_authors  
```
create view v_authors as 
select authors.name as author, articles.title from authors 
left join articles on authors.id = articles.author;  
```

- v_percentage  
```
create view v_percentage as 
select  
to_char(date_trunc('day', time), 'yyyy-mm-dd') as day, 
   cast(  
		sum(case when status = '200 OK' then 0 else 1 end) as float  
		)   
	/  
	(  
	sum(case when status = '200 OK' then 1 else 0 end) +  
	sum(case when status = '200 OK' then 0 else 1 end)  
	)   
as percentage  
from log  
group by day 
order by percentage desc;  
```



## Usage

``` bash
vagrant@vagrant:/vagrant/Udacity_FullStackWebDeveloper_P1$ python log_analysis.py
What are the most popular three articles of all time?
        Candidate is jerk, alleges rival: 338,647
        Bears love berries, alleges bear: 253,801
        Bad things gone, say good people: 170,098
Who are the most popular article authors of all time?
        ['Ursula La Multa', 'Rudolf von Treppenwitz', 'Anonymous Contributor']
On which days did more than 1% of requests lead to errors?
        2016-07-17: 2.26%
```

## Author

[mrsmmori](https://github.com/mrsmmori)

