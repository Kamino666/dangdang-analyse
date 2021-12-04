# dangdang-analyse
爬取、分析当当网的图书评论数据，用来做大作业的

## API分析

GET http://product.dangdang.com/index.php?r=comment%2Flist&productId=25205774&pageIndex=1&sortType=1&filterType=1&tagId=0&tagFilterCount=0

基础URL：http://product.dangdang.com/index.php?r=comment%2Flist

**参数**
+ productId: 商品的id
+ pageIndex: 评论分页 只能获取前200页
+ sortType: 精彩评论1 时间排序2
+ filterType: 全部1 好评2 中评3 差评4 晒图5
+ tagId和tagFilterCount: 关键词过滤，这里用不着就不分析了

**HTTP Header**

Host和Referer填好，加上老生常谈的User-Agent就行了。
+ 'Host': "product.dangdang.com",
+ 'Referer': "http://product.dangdang.com/22765017.html",

**返回**

返回json文本，`list`属性对应的值是评论短评，`longlist`对应的是长评，本库只关注短评.

评论的数据格式是html，每一条评论用`<div class="comment_items clearfix">`包裹。

假如爬取完评论了，则返回的html中定位不到`class="fanye_box"`这个元素

