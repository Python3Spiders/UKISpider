import matplotlib.pyplot as plt
import jieba
from scipy.misc import imread
from wordcloud import WordCloud

# 导入filename文件里的分词，并返回
def importStopword(filename=''):
	stopwords = {}
	f = open(filename, 'r', encoding='utf-8')
	line = f.readline().rstrip()
	while line:
		stopwords.setdefault(line, 0)
		stopwords[line] = 1
		line = f.readline().rstrip()
	f.close()
	return stopwords

# 根据导入的分词拆分中文
def processChinese(text, stopwords):
	seg_generator = jieba.cut(text)
	seg_list = [i for i in seg_generator if i not in stopwords]
	seg_list = [i for i in seg_list if i != u' ']
	seg_list = r' '.join(seg_list)
	return seg_list

def painter():
	# 待生成词云的文本内容
	text = open('sign.txt', encoding="utf-8").read()
	# 加载分词
	stopwords = importStopword(filename='./StopWords.txt')
	# 得到分词处理结果
	text = processChinese(text, stopwords)
	# 加载词云背景图片
	back_colorimg = imread("./wordcloud_background/bc.png")
	# 根据字体、背景色等创建词云对象
	WC = WordCloud(
		font_path='my_font.ttf',
		background_color="#ffffff",
		max_words=2000,
		mask=back_colorimg,
		random_state=42
	)
	# 词云对象加载分词结果
	WC.generate(text)
	plt.figure('Sign')
	plt.imshow(WC)
	plt.axis("off")
	#显示词云图
	plt.show()
	# 将词云图保持到文件
	WC.to_file("nickname.png")

if __name__ == '__main__':
	painter()