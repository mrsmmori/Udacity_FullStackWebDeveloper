
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


## Prerequisit in postgresql
Setup below 3 view(s) and 1 table in news database.

### View(s)

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

### Table  
```
create table map (
 log_title varchar (255) primary key,
 article_title varchar (255) not null,
 description varchar (255),
 rel varchar (50)
);
insert into map (log_title, article_title) 
values 
('bad-things-gone', 'Bad things gone, say good people'),
('balloon-goons-doomed', 'Balloon goons doomed'),
('bears-love-berries', 'Bears love berries, alleges bear'),
('candidate-is-jerk', 'Candidate is jerk, alleges rival'),
('goats-eat-googles', 'Goats eat Google''s lawn'),
('media-obsessed-with-bears', 'Media obsessed with bears'),
('trouble-for-troubled', 'Trouble for troubled troublemakers'),
('so-many-bears', 'There are a lot of bears');
```

## Usage

```
vagrant@vagrant:~$ python log_analysis.py
What are the most popular three articles of all time?
        Candidate is jerk, alleges rival: 338,647
        Bears love berries, alleges bear: 253,801
        Bad things gone, say good people: 170,098
Who are the most popular article authors of all time?
        Ursula La Multa: 507,594
On which days did more than 1% of requests lead to errors?
        2016-07-17: 2.26%
vagrant@vagrant:~$
```

## Author

[mrsmmori](https://github.com/mrsmmori)

