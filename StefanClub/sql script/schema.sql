-- schema.sql

drop database if exists stefan;

create database stefan;

use stefan;

grant select, insert, update, delete on stefan.* to 'root'@'localhost' identified by 'Kaihua1010';

create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `passwd` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table blogs (
    `id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `name` varchar(50) not null,
    `summary` varchar(200) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table comments (
    `id` varchar(50) not null,
    `blog_id` varchar(50) not null,
    `user_id` varchar(50) not null,
    `user_name` varchar(50) not null,
    `user_image` varchar(500) not null,
    `content` mediumtext not null,
    `created_at` real not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table IndexCarouselItems (
    `id` int not null auto_increment,
    `number` int not null,
    `title` varchar(300) not null,
    `url` varchar(300) not null,
    `img_url` varchar(300) not null,
    `item_class`  varchar(10) not null,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table IndexNews (
    `id` int not null auto_increment,
    `number` int not null,
    `close_target_id` varchar(20) not null,
    `close_target_id_ref` varchar(20) not null,
    `title` varchar(300) not null,
    `url` varchar(300) not null,
    `news_summary` varchar(300) not null,
    `user_img_url` varchar(300) not null,
    `user_name`  varchar(50) not null,
    `news_date`  varchar(100) not null,
    `news_label`  varchar(50),
    `news_reads`  int not null,
    `news_comments` int not null,
    `hate_emails` varchar(3000),
    `user_url` varchar(300) not null,
    `label_url` varchar(300) not null,
    `comment_url` varchar(300) not null,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;


create table HotMatches (
    `id` int not null auto_increment,
    `type` varchar(50) not null ,
    `livecast_id` varchar(100) not null ,
    `title` varchar(300) not null,
    `team1` varchar(50) not null,
    `team2` varchar(50) not null,
    `score1` varchar(5)  ,
    `score2` varchar(5)  ,
    `matchdate`  varchar(100) ,
    `matchtime`  varchar(100) ,
    `newsurl` varchar(300) ,
    `liveurl` varchar(300) ,
    `match_url` varchar(300) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table SinaCarousel (
    `id` int not null auto_increment,
    `number` int not null,
    `title` varchar(300) not null,
    `url` varchar(300) not null,
    `img_url` varchar(300) not null,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table HotMatchNews (
    `id` int not null auto_increment,
    `number` int not null,
    `title1` varchar(300) ,
    `title2` varchar(300) ,
    `title3` varchar(300) ,
    `title1url` varchar(300) ,
    `title2url` varchar(300) ,
    `title3url` varchar(300) ,
    `imgsrcurl` varchar(300) not null,
    `imgurl` varchar(300) not null,
    `line1` varchar(300) ,
    `line2` varchar(300) ,
    `line3` varchar(300) ,
    `line4` varchar(300) ,
    `line5` varchar(300) ,
    `line6` varchar(300) ,
    `line7` varchar(300) ,
    `line8` varchar(300) ,
    `line9` varchar(300) ,
    `line1url` varchar(300) ,
    `line2url` varchar(300) ,
    `line3url` varchar(300) ,
    `line4url` varchar(300) ,
    `line5url` varchar(300) ,
    `line6url` varchar(300) ,
    `line7url` varchar(300) ,
    `line8url` varchar(300) ,
    `line9url` varchar(300) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table NbaNews (
    `id` int not null auto_increment,
    `newstype` varchar(300),
    `number` int,
    `imgsrcurl` varchar(300),
    `imgurl` varchar(300),
    `isvideo` varchar(5),
    `title` varchar(300) ,
    `titleurl` varchar(300) ,
    `newstime` DATETIME ,
    `comment_url` varchar(300) ,
    `tag1` varchar(300) ,
    `tag2` varchar(300) ,
    `tag3` varchar(300) ,
    `tag4` varchar(300) ,
    `tag5` varchar(300) ,
    `tag1url` varchar(300) ,
    `tag2url` varchar(300) ,
    `tag3url` varchar(300) ,
    `tag4url` varchar(300) ,
    `tag5url` varchar(300) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;


create table ZhihuHot (
    `id` int not null auto_increment,
    `hotid` varchar(30) not null,
    `collapse_no` varchar(20),
    `collapse_no_ref` varchar(20),
    `feedsourcetag` varchar(100),
    `feedsourceurl` varchar(300),
    `userimgnumber` int,
    `userimgsrcurl` varchar(300),
    `userimgurl` varchar(300),
    `username` varchar(100),
    `userinfo` varchar(300),
    `newsimgnumber` int,
    `newsimgsrcurl` varchar(300),
    `newsimgurl` varchar(300),
    `isvideo` varchar(5),
    `title` varchar(300) ,
    `titleurl` varchar(300) ,
    `newscontent` varchar(1000) ,
    `infavorqty`  varchar(20) ,
    `comment_url` varchar(300) ,
    `comment_title` varchar(300) ,
    `share_url` varchar(300) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

create table ZhihuHot_Comment (
    `id` int not null auto_increment,
    `commentid` varchar(30) not null,
    `hotid` varchar(30) not null,
    `userimgnumber` int,
    `userimgsrcurl` varchar(300),
    `userimgurl` varchar(300),
    `username` varchar(100),
    `replytouser` varchar(100),
    `replytouserurl` varchar(300),
    `replytime` varchar(50),
    `content` varchar(1000) ,
    `infavorqty`  varchar(20) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;


create table TaobaoProducts (
    `id` int not null auto_increment,
    `keyword` varchar(30) not null,
    `product_id` varchar(100),
    `product_type` varchar(100),
    `imgsrcurl` varchar(300),
    `imgurl` varchar(300),
    `imgnumber` int,
    `samestyleurl` varchar(300),
    `similarurl` varchar(300),
    `product_price` varchar(20),
    `payednum`  varchar(20) ,
    `title` varchar(300),
    `titleurl` varchar(300),
    `shopname` varchar(100),
    `shopurl` varchar(300),
    `shopaddress` varchar(20) ,
    `shoplevelzuanqty` int,
    `shoplevelguanqty` int,
    `shoplevelxinqty` int,
    `shopleveljingguanqty` int,
    `istmall` varchar(10),
    `iconkey1` varchar(100),
    `icontitle1` varchar(100),
    `iconurl1` varchar(300),
    `iconkey2` varchar(100),
    `icontitle2` varchar(100),
    `iconurl2` varchar(300),
    `iconkey3` varchar(100),
    `icontitle3` varchar(100),
    `iconurl3` varchar(300),
    `iconkey4` varchar(100),
    `icontitle4` varchar(100),
    `iconurl4` varchar(300),
    `iconkey5` varchar(100),
    `icontitle5` varchar(100),
    `iconurl5` varchar(300),
    `subiconclass1` varchar(100),
    `subicontitle1` varchar(100),
    `subiconcontent1` varchar(300),
    `subiconclass2` varchar(100),
    `subicontitle2` varchar(100),
    `subiconcontent2` varchar(300),
    `subiconclass3` varchar(100),
    `subicontitle3` varchar(100),
    `subiconcontent3` varchar(300),
    `subiconclass4` varchar(100),
    `subicontitle4` varchar(100),
    `subiconcontent4` varchar(300),
    `subiconclass5` varchar(100),
    `subicontitle5` varchar(100),
    `subiconcontent5` varchar(300),
    `shoptotalrate` varchar(20),
    `shopdescscore` varchar(20),
    `shopdescscorediff` varchar(20) ,
    `shopdesccompare` varchar(20) ,
    `shopdeliveryscore` varchar(20),
    `shopdeliveryscorediff` varchar(20) ,
    `shopdeliverycompare` varchar(20) ,
    `shopservicescore` varchar(20),
    `shopservicescorediff` varchar(20) ,
    `shopservicecompare` varchar(20) ,
    `created_at` TIMESTAMP not null,
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;