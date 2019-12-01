DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS blog;
DROP TABLE IF EXISTS USER;

CREATE TABLE user (
  id          INT PRIMARY KEY  AUTO_INCREMENT,
  username    VARCHAR(50) NOT NULL UNIQUE,
  nickname    VARCHAR(50) NOT NULL,
  password    VARCHAR(20) NOT NULL,
  update_time DATETIME,
  is_enable   BOOLEAN
)
  CHARACTER SET utf8
  COLLATE utf8_general_ci;

CREATE TABLE blog (
  id           INT PRIMARY KEY AUTO_INCREMENT,
  update_time  DATETIME,
  blog_content TEXT,
  user_id      INT,
  is_deleted   BOOLEAN,
  FOREIGN KEY (user_id) REFERENCES user (id)
)
  CHARACTER SET utf8
  COLLATE utf8_general_ci;

CREATE TABLE comment (
  id              INT PRIMARY KEY  AUTO_INCREMENT,
  blog_id         INT,
  update_time     DATETIME,
  comment_content TEXT,
  is_deleted      BOOLEAN,
  user_id         INT,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (blog_id) REFERENCES blog (id)
)
  CHARACTER SET utf8
  COLLATE utf8_general_ci;