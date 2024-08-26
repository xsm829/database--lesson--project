CREATE TABLE zhihu (
  url varchar(255) DEFAULT NULL,
  question_title varchar(255) DEFAULT NULL,
  question_text varchar(5000) DEFAULT NULL,
  followers varchar(255) DEFAULT NULL,
  views varchar(255) DEFAULT NULL,
  likes varchar(255) DEFAULT NULL,
  topics1 varchar(255) DEFAULT NULL,
  topics2 varchar(255) DEFAULT NULL,
  topics3 varchar(255) DEFAULT NULL,
  topics4 varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""
CREATE TABLE book_country_num (
  country varchar(255) DEFAULT NULL COMMENT '����',
  num int(11) DEFAULT NULL COMMENT '����'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE book_publisher_num (
  publisher varchar(255) DEFAULT NULL COMMENT '������',
  num int(11) DEFAULT NULL COMMENT '����'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE book_presstime_num (
  press_time int(11) DEFAULT NULL COMMENT '����ʱ��',
  num int(11) DEFAULT NULL COMMENT '����'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE book_people_title (
  people int(11) DEFAULT NULL COMMENT '��������',
  title varchar(255) DEFAULT NULL COMMENT '����'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE book_score_num (
  score float DEFAULT NULL COMMENT '����',
  num int(11) DEFAULT NULL COMMENT '����'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
"""


insert into book_country_num
  select
  country, count(*) as num
  from books
  group by country;

...... 