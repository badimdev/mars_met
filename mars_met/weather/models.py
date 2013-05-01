from django.db import models
from datetime import datetime, timedelta
from math import *

class position():
	angle=0.00
	xAxis=0
	yAxis=0

class report(models.Model):
	sol=models.IntegerField(primary_key=True)
	terrestrial_date=models.DateTimeField(null=True)

	def __unicode__(self):
		return str(self.sol)

	def _get_earth_position(self):
		
		year=self.terrestrial_date.year
		perihelion=datetime(year,01,02,00,00,00)
		substraction=self.terrestrial_date.replace(tzinfo=None)-perihelion
		seconds=substraction.total_seconds()
		
		n = 2 * pi / (365.256*86400)
		m = n * seconds
		e = m
		exc = 0.01679
		e1 = m + exc*sin(e)

		while(abs(e1-e) > 0.00001):
			e = e1
			e1 = m + exc*sin(e)

		argument = sqrt( (1 + exc) / (1 - exc) )
		pos = argument * tan(e/2)
		angle = 2*atan(pos)
		data=position()
		data.xAxis='%.4f' % (cos(angle)*1)
		data.yAxis='%.4f' % (sin(angle)*1)
		data.angle='%.4f' % (90 - degrees(angle))
		return data
	
	earth_position=property(_get_earth_position)

class magnitude(models.Model):
	sol=models.ForeignKey('report',db_column='sol',primary_key=True)
	min_temp=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	max_temp=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	pressure=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	pressure_string=models.CharField(max_length=64, null=True)
	abs_humidity=models.CharField(max_length=64, null=True)
	wind_speed=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	wind_direction=models.CharField(max_length=16, null=True)
	atmo_opacity=models.CharField(max_length=64, null=True)
	season=models.CharField(max_length=64, null=True)
	ls=models.DecimalField(max_digits=6, decimal_places=2, null=True)
	sunrise=models.CharField(max_length=16, null=True)
	sunset=models.CharField(max_length=16, null=True)
	
	def __unicode__(self):
		return self.sol.terrestrial_date.strftime('%Y-%m-%d')

	def _get_avg_temp(self):

		avg_temp = (self.min_temp + self.max_temp) / 2
		
		return(avg_temp)

	def _get_mars_position(self):
		
		angle = float(self.ls)
		data=position()
		data.xAxis='%.4f' % (cos(radians(angle))*1.52)
		data.yAxis='%.4f' % (sin(radians(angle))*1.52)
		data.angle='%.4f' % angle
		return data

	mars_position = property(_get_mars_position)
	avg_temp = property(_get_avg_temp)