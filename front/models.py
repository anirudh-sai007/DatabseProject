from django.db import models


class  FALL22_S003_14_USER_TYPES(models.Model):
    id=models.AutoField(primary_key = True, null = False, blank = True)
    type=models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'FALL22_S003_14_USER_TYPES'

class FALL22_S003_14_USERS(models.Model):
    id = models.AutoField(primary_key = True, null = False, blank = True)
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    email_id=models.CharField(max_length=50)
    is_vaccinated=models.BigIntegerField()
    fk_user_type_id=models.ForeignKey(FALL22_S003_14_USER_TYPES, models.DO_NOTHING, db_column='fk_user_type_id',related_name='user_type_id')
    class Meta:
        managed = False
        db_table = 'FALL22_S003_14_USERS'

class FALL22_S003_14_BOOKINGS(models.Model):
    id = models.AutoField(primary_key = True, null = False, blank = True)
    fk_customer_id=models.ForeignKey('FALL22_S003_14_USERS', models.DO_NOTHING, db_column='fk_customer_id',related_name='customer_id')
    fk_service_provider_id=models.ForeignKey('FALL22_S003_14_USERS', models.DO_NOTHING, db_column='fk_service_provider_id',related_name='service_provider_id')
    decription=models.CharField(max_length=100)
    charges=models.DecimalField(decimal_places=3,max_digits=3)
    status=models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'FALL22_S003_14_BOOKINGS'

class FALL22_S003_14_FEEDBACK(models.Model):
    id= models.AutoField(primary_key = True, null = False, blank = True)
    fk_booking_id=models.ForeignKey(FALL22_S003_14_USERS, models.DO_NOTHING, db_column='fk_booking_id',related_name='booking_id')
    comments=models.CharField(max_length=100)
    rating=models.BigIntegerField()


