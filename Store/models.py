from django.db import models

# Create your models here.
# 定义卖家模型类
class Seller(models.Model):
    username = models.CharField(max_length=32,verbose_name="用户名")
    password = models.CharField(max_length=32,verbose_name="密码")
    nickname = models.CharField(max_length=32,verbose_name="昵称",null=True,blank=True)
    phone = models.CharField(max_length=32,verbose_name="手机",null=True,blank=True)
    email = models.EmailField(verbose_name="邮箱",null=True,blank=True)
    picture = models.ImageField(upload_to="store/images",verbose_name="头像",null=True,blank=True)
    address = models.CharField(max_length=32,verbose_name="地址",null=True,blank=True)

    card_id = models.CharField(max_length=32,verbose_name="身份证",null=True,blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "卖家"
        verbose_name_plural = "卖家"

# 定义店铺类型类
class StoreType(models.Model):
    store_type = models.CharField(max_length=32,verbose_name="类型名称")
    type_description = models.TextField(verbose_name="类型描述")

    def __str__(self):
        return self.store_type

    class Meta:
        verbose_name = "店铺类型"
        verbose_name_plural = "店铺类型"

# 定义店铺类
class Store(models.Model):
    store_name = models.CharField(max_length=32,verbose_name="店铺名称")
    store_address = models.CharField(max_length=32,verbose_name="店铺地址")
    store_description = models.TextField(verbose_name="店铺描述")
    store_logo = models.ImageField(upload_to="store/images",verbose_name="店铺logo")
    store_phone = models.CharField(max_length=32,verbose_name="店铺电话")
    store_money = models.FloatField(verbose_name="店铺注册资金")

    user_id = models.IntegerField(verbose_name="店铺主人")
    type = models.ManyToManyField(to=StoreType,verbose_name="店铺类型")

    def __str__(self):
        return self.store_name

    class Meta:
        verbose_name = "店铺"
        verbose_name_plural = "店铺"

from django.db.models import Manager
import datetime
class GoodsTypeManage(Manager):
    def addType(self,name,picture = "buyer/images/banner05.jpg"):
        goods_type = GoodsType()
        goods_type.name = name
        now = datetime.datetime.now().strftime("%Y-%m-%d")
        goods_type.description = "%s_%s"%(now,name)
        goods_type.picture = picture
        goods_type.save()
        return goods_type

# v2.6 新增商品类型
class GoodsType(models.Model):
    name = models.CharField(max_length=32,verbose_name="商品类型名称")
    description = models.TextField(verbose_name="商品类型描述")
    picture = models.ImageField(upload_to="buyer/images",verbose_name="商品类型首页展示图片")
    objects = GoodsTypeManage()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品类型"
        verbose_name_plural = "商品类型"

class GoodsManage(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(goods_price=24)
    # def all(self):
    #     """
    #     查询所有香蕉
    #     """
    #     return super().all().filter(goods_name='香蕉')

    def up_goods(self):
        """
        全部上架的商品
        :return:
        """
        return Goods.objects.filter(goods_under=1)

# 定义商品类
class Goods(models.Model):
    goods_name = models.CharField(max_length=32,verbose_name="商品名称")
    goods_price = models.FloatField(verbose_name="商品价格")
    goods_image = models.ImageField(upload_to="store/images",verbose_name="商品图片")
    goods_number = models.IntegerField(verbose_name="商品库存")
    goods_description = models.TextField(verbose_name="商品描述")
    goods_date = models.DateField(verbose_name="出厂日期",null=True,blank=True)
    goods_safeDate = models.IntegerField(verbose_name="保质期")
    # v2.4 新增商品状态字段;1 待售 0 下架
    goods_under = models.IntegerField(verbose_name="商品状态",default=1)
    # v2.6 新增商品类型对应商品类型表
    goods_type = models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,verbose_name="商品类型")
    # v3.6 修改商铺商品为一对多关系
    store_id = models.ForeignKey(to=Store,on_delete=models.CASCADE,verbose_name="商品店铺")


    def __str__(self):
        return self.goods_name

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = "商品"

# 定义商品图片类
class GoodsImg(models.Model):
    img_address = models.ImageField(upload_to="store/images",verbose_name="图片地址")
    img_description = models.TextField(verbose_name="图片描述")
    goods_id = models.ForeignKey(to=Goods,on_delete=models.CASCADE,verbose_name="商品id")

    def __str__(self):
        return self.img_address

    class Meta:
        verbose_name = "商品图片"
        verbose_name_plural = "商品图片"
