/*
 Navicat Premium Data Transfer

 Source Server         : homestead
 Source Server Type    : MySQL
 Source Server Version : 50719
 Source Host           : 192.168.10.10:3306
 Source Schema         : spider

 Target Server Type    : MySQL
 Target Server Version : 50719
 File Encoding         : 65001

 Date: 05/02/2018 19:05:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for db_book
-- ----------------------------
DROP TABLE IF EXISTS `db_book`;
CREATE TABLE `db_book`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '书籍名',
  `book_img` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '书籍封面',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '书籍url',
  `subject_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '豆瓣书籍id',
  `isbn` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT 'ISBN',
  `author` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '作者名',
  `publisher` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '出版社',
  `publication_year` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '出版年份',
  `pages` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '页数',
  `price` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '0.00' COMMENT '定价',
  `layout` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '装帧',
  `grade` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '豆瓣评分',
  `graded_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '评分人数',
  `five_graded_percent` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '五星评分占比',
  `four_graded_percent` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '四星评分占比',
  `three_graded_percent` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '三星评分占比',
  `two_graded_percent` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '两星评分占比',
  `one_graded_percent` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '一星评分占比',
  `short_comment_count` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '短评数',
  `book_review_count` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '书评数',
  `note_count` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '读书笔记数',
  `create_time` int(10) UNSIGNED NOT NULL,
  `update_time` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `subject_id`(`subject_id`) USING BTREE COMMENT '唯一索引'
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for db_book_tag
-- ----------------------------
DROP TABLE IF EXISTS `db_book_tag`;
CREATE TABLE `db_book_tag`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '标签名',
  `pid` int(10) UNSIGNED NOT NULL COMMENT '上级id',
  `url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '此分类url',
  `book_count` bigint(20) UNSIGNED NOT NULL COMMENT '分类书籍数量',
  `create_time` int(10) UNSIGNED NOT NULL,
  `update_time` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 152 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of db_book_tag
-- ----------------------------
INSERT INTO `db_book_tag` VALUES (1, '文学', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (2, '小说', 1, 'https://book.douban.com/tag//tag/小说', 4906071, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (3, '外国文学', 1, 'https://book.douban.com/tag//tag/外国文学', 1748312, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (4, '文学', 1, 'https://book.douban.com/tag//tag/文学', 1381465, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (5, '随笔', 1, 'https://book.douban.com/tag//tag/随笔', 1050291, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (6, '中国文学', 1, 'https://book.douban.com/tag//tag/中国文学', 933785, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (7, '经典', 1, 'https://book.douban.com/tag//tag/经典', 819246, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (8, '日本文学', 1, 'https://book.douban.com/tag//tag/日本文学', 737535, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (9, '散文', 1, 'https://book.douban.com/tag//tag/散文', 639401, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (10, '村上春树', 1, 'https://book.douban.com/tag//tag/村上春树', 413553, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (11, '诗歌', 1, 'https://book.douban.com/tag//tag/诗歌', 298419, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (12, '童话', 1, 'https://book.douban.com/tag//tag/童话', 276621, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (13, '儿童文学', 1, 'https://book.douban.com/tag//tag/儿童文学', 213372, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (14, '古典文学', 1, 'https://book.douban.com/tag//tag/古典文学', 211056, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (15, '王小波', 1, 'https://book.douban.com/tag//tag/王小波', 209069, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (16, '杂文', 1, 'https://book.douban.com/tag//tag/杂文', 205677, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (17, '名著', 1, 'https://book.douban.com/tag//tag/名著', 198845, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (18, '余华', 1, 'https://book.douban.com/tag//tag/余华', 186987, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (19, '张爱玲', 1, 'https://book.douban.com/tag//tag/张爱玲', 182647, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (20, '当代文学', 1, 'https://book.douban.com/tag//tag/当代文学', 128226, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (21, '钱钟书', 1, 'https://book.douban.com/tag//tag/钱钟书', 98366, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (22, '外国名著', 1, 'https://book.douban.com/tag//tag/外国名著', 86167, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (23, '鲁迅', 1, 'https://book.douban.com/tag//tag/鲁迅', 82979, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (24, '诗词', 1, 'https://book.douban.com/tag//tag/诗词', 71941, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (25, '茨威格', 1, 'https://book.douban.com/tag//tag/茨威格', 58872, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (26, '米兰·昆德拉', 1, 'https://book.douban.com/tag//tag/米兰·昆德拉', 50929, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (27, '杜拉斯', 1, 'https://book.douban.com/tag//tag/杜拉斯', 43035, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (28, '港台', 1, 'https://book.douban.com/tag//tag/港台', 6960, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (29, '流行', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (30, '漫画', 1, 'https://book.douban.com/tag//tag/漫画', 1213291, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (31, '推理', 1, 'https://book.douban.com/tag//tag/推理', 863798, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (32, '绘本', 1, 'https://book.douban.com/tag//tag/绘本', 846496, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (33, '青春', 1, 'https://book.douban.com/tag//tag/青春', 622332, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (34, '东野圭吾', 1, 'https://book.douban.com/tag//tag/东野圭吾', 506383, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (35, '科幻', 1, 'https://book.douban.com/tag//tag/科幻', 482070, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (36, '言情', 1, 'https://book.douban.com/tag//tag/言情', 472523, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (37, '悬疑', 1, 'https://book.douban.com/tag//tag/悬疑', 437691, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (38, '奇幻', 1, 'https://book.douban.com/tag//tag/奇幻', 301417, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (39, '武侠', 1, 'https://book.douban.com/tag//tag/武侠', 299409, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (40, '日本漫画', 1, 'https://book.douban.com/tag//tag/日本漫画', 271554, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (41, '韩寒', 1, 'https://book.douban.com/tag//tag/韩寒', 261505, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (42, '耽美', 1, 'https://book.douban.com/tag//tag/耽美', 240950, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (43, '亦舒', 1, 'https://book.douban.com/tag//tag/亦舒', 233052, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (44, '推理小说', 1, 'https://book.douban.com/tag//tag/推理小说', 227337, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (45, '三毛', 1, 'https://book.douban.com/tag//tag/三毛', 198512, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (46, '网络小说', 1, 'https://book.douban.com/tag//tag/网络小说', 196987, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (47, '安妮宝贝', 1, 'https://book.douban.com/tag//tag/安妮宝贝', 172394, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (48, '郭敬明', 1, 'https://book.douban.com/tag//tag/郭敬明', 152441, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (49, '穿越', 1, 'https://book.douban.com/tag//tag/穿越', 148537, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (50, '金庸', 1, 'https://book.douban.com/tag//tag/金庸', 144628, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (51, '阿加莎·克里斯蒂', 1, 'https://book.douban.com/tag//tag/阿加莎·克里斯蒂', 142598, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (52, '轻小说', 1, 'https://book.douban.com/tag//tag/轻小说', 138034, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (53, '科幻小说', 1, 'https://book.douban.com/tag//tag/科幻小说', 122961, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (54, '几米', 1, 'https://book.douban.com/tag//tag/几米', 114302, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (55, '青春文学', 1, 'https://book.douban.com/tag//tag/青春文学', 112248, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (56, '魔幻', 1, 'https://book.douban.com/tag//tag/魔幻', 109630, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (57, '幾米', 1, 'https://book.douban.com/tag//tag/幾米', 97704, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (58, '张小娴', 1, 'https://book.douban.com/tag//tag/张小娴', 97538, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (59, 'J.K.罗琳', 1, 'https://book.douban.com/tag//tag/J.K.罗琳', 82918, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (60, '古龙', 1, 'https://book.douban.com/tag//tag/古龙', 73077, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (61, '高木直子', 1, 'https://book.douban.com/tag//tag/高木直子', 71705, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (62, '沧月', 1, 'https://book.douban.com/tag//tag/沧月', 65133, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (63, '落落', 1, 'https://book.douban.com/tag//tag/落落', 58460, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (64, '校园', 1, 'https://book.douban.com/tag//tag/校园', 57772, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (65, '张悦然', 1, 'https://book.douban.com/tag//tag/张悦然', 57570, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (66, '文化', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (67, '历史', 1, 'https://book.douban.com/tag//tag/历史', 1867520, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (68, '心理学', 1, 'https://book.douban.com/tag//tag/心理学', 1219538, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (69, '哲学', 1, 'https://book.douban.com/tag//tag/哲学', 1015623, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (70, '传记', 1, 'https://book.douban.com/tag//tag/传记', 717400, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (71, '文化', 1, 'https://book.douban.com/tag//tag/文化', 656307, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (72, '社会学', 1, 'https://book.douban.com/tag//tag/社会学', 604367, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (73, '艺术', 1, 'https://book.douban.com/tag//tag/艺术', 446771, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (74, '设计', 1, 'https://book.douban.com/tag//tag/设计', 377596, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (75, '社会', 1, 'https://book.douban.com/tag//tag/社会', 347165, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (76, '政治', 1, 'https://book.douban.com/tag//tag/政治', 327911, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (77, '建筑', 1, 'https://book.douban.com/tag//tag/建筑', 255935, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (78, '宗教', 1, 'https://book.douban.com/tag//tag/宗教', 233043, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (79, '电影', 1, 'https://book.douban.com/tag//tag/电影', 225434, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (80, '数学', 1, 'https://book.douban.com/tag//tag/数学', 203067, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (81, '政治学', 1, 'https://book.douban.com/tag//tag/政治学', 198485, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (82, '回忆录', 1, 'https://book.douban.com/tag//tag/回忆录', 157807, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (83, '中国历史', 1, 'https://book.douban.com/tag//tag/中国历史', 153981, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (84, '思想', 1, 'https://book.douban.com/tag//tag/思想', 142972, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (85, '国学', 1, 'https://book.douban.com/tag//tag/国学', 133358, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (86, '人文', 1, 'https://book.douban.com/tag//tag/人文', 113476, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (87, '音乐', 1, 'https://book.douban.com/tag//tag/音乐', 112223, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (88, '人物传记', 1, 'https://book.douban.com/tag//tag/人物传记', 109360, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (89, '绘画', 1, 'https://book.douban.com/tag//tag/绘画', 102786, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (90, '艺术史', 1, 'https://book.douban.com/tag//tag/艺术史', 101032, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (91, '戏剧', 1, 'https://book.douban.com/tag//tag/戏剧', 98402, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (92, '佛教', 1, 'https://book.douban.com/tag//tag/佛教', 66132, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (93, '军事', 1, 'https://book.douban.com/tag//tag/军事', 65388, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (94, '二战', 1, 'https://book.douban.com/tag//tag/二战', 64032, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (95, '西方哲学', 1, 'https://book.douban.com/tag//tag/西方哲学', 63558, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (96, '近代史', 1, 'https://book.douban.com/tag//tag/近代史', 58443, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (97, '考古', 1, 'https://book.douban.com/tag//tag/考古', 46346, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (98, '自由主义', 1, 'https://book.douban.com/tag//tag/自由主义', 41707, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (99, '美术', 1, 'https://book.douban.com/tag//tag/美术', 34028, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (100, '生活', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (101, '爱情', 1, 'https://book.douban.com/tag//tag/爱情', 800921, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (102, '旅行', 1, 'https://book.douban.com/tag//tag/旅行', 544643, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (103, '生活', 1, 'https://book.douban.com/tag//tag/生活', 474123, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (104, '成长', 1, 'https://book.douban.com/tag//tag/成长', 451287, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (105, '励志', 1, 'https://book.douban.com/tag//tag/励志', 367214, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (106, '心理', 1, 'https://book.douban.com/tag//tag/心理', 346133, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (107, '摄影', 1, 'https://book.douban.com/tag//tag/摄影', 277248, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (108, '女性', 1, 'https://book.douban.com/tag//tag/女性', 268236, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (109, '职场', 1, 'https://book.douban.com/tag//tag/职场', 194005, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (110, '教育', 1, 'https://book.douban.com/tag//tag/教育', 185559, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (111, '美食', 1, 'https://book.douban.com/tag//tag/美食', 181315, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (112, '游记', 1, 'https://book.douban.com/tag//tag/游记', 143959, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (113, '灵修', 1, 'https://book.douban.com/tag//tag/灵修', 118144, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (114, '健康', 1, 'https://book.douban.com/tag//tag/健康', 74225, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (115, '情感', 1, 'https://book.douban.com/tag//tag/情感', 73651, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (116, '手工', 1, 'https://book.douban.com/tag//tag/手工', 39546, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (117, '两性', 1, 'https://book.douban.com/tag//tag/两性', 38265, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (118, '养生', 1, 'https://book.douban.com/tag//tag/养生', 34219, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (119, '人际关系', 1, 'https://book.douban.com/tag//tag/人际关系', 32911, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (120, '家居', 1, 'https://book.douban.com/tag//tag/家居', 21098, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (121, '自助游', 1, 'https://book.douban.com/tag//tag/自助游', 2640, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (122, '经管', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (123, '经济学', 1, 'https://book.douban.com/tag//tag/经济学', 386972, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (124, '管理', 1, 'https://book.douban.com/tag//tag/管理', 379462, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (125, '经济', 1, 'https://book.douban.com/tag//tag/经济', 309719, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (126, '商业', 1, 'https://book.douban.com/tag//tag/商业', 269538, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (127, '金融', 1, 'https://book.douban.com/tag//tag/金融', 251757, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (128, '投资', 1, 'https://book.douban.com/tag//tag/投资', 202720, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (129, '营销', 1, 'https://book.douban.com/tag//tag/营销', 141340, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (130, '创业', 1, 'https://book.douban.com/tag//tag/创业', 102769, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (131, '理财', 1, 'https://book.douban.com/tag//tag/理财', 99298, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (132, '广告', 1, 'https://book.douban.com/tag//tag/广告', 61755, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (133, '股票', 1, 'https://book.douban.com/tag//tag/股票', 58305, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (134, '企业史', 1, 'https://book.douban.com/tag//tag/企业史', 18732, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (135, '策划', 1, 'https://book.douban.com/tag//tag/策划', 7943, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (136, '科技', 0, '', 0, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (137, '科普', 1, 'https://book.douban.com/tag//tag/科普', 515455, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (138, '互联网', 1, 'https://book.douban.com/tag//tag/互联网', 219950, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (139, '编程', 1, 'https://book.douban.com/tag//tag/编程', 145869, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (140, '科学', 1, 'https://book.douban.com/tag//tag/科学', 117970, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (141, '交互设计', 1, 'https://book.douban.com/tag//tag/交互设计', 65024, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (142, '用户体验', 1, 'https://book.douban.com/tag//tag/用户体验', 51890, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (143, '算法', 1, 'https://book.douban.com/tag//tag/算法', 47932, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (144, '科技', 1, 'https://book.douban.com/tag//tag/科技', 22608, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (145, 'web', 1, 'https://book.douban.com/tag//tag/web', 21355, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (146, 'UE', 1, 'https://book.douban.com/tag//tag/UE', 4945, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (147, '通信', 1, 'https://book.douban.com/tag//tag/通信', 4588, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (148, '交互', 1, 'https://book.douban.com/tag//tag/交互', 4585, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (149, 'UCD', 1, 'https://book.douban.com/tag//tag/UCD', 3526, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (150, '神经网络', 1, 'https://book.douban.com/tag//tag/神经网络', 2218, 1516255421, 1516255421);
INSERT INTO `db_book_tag` VALUES (151, '程序', 1, 'https://book.douban.com/tag//tag/程序', 1243, 1516255421, 1516255421);

-- ----------------------------
-- Table structure for db_book_tag_relation
-- ----------------------------
DROP TABLE IF EXISTS `db_book_tag_relation`;
CREATE TABLE `db_book_tag_relation`  (
  `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `book_id` int(10) UNSIGNED NOT NULL COMMENT '书籍id',
  `tag_id` int(10) UNSIGNED NOT NULL COMMENT '热门标签id',
  `create_time` int(10) UNSIGNED NOT NULL,
  `update_time` int(10) UNSIGNED NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
