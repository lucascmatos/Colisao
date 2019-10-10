#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import PointCloud
from array import array
from math import atan2,degrees
vetx = []#Vetores de pontos
vety = []
vetz = []
sum_root = 0 # soma dos quadrados dos pontos
i = 0
aux_x = 0# auxiliar da variavel x para append
aux_y = 0# auxiliar da variavel y para append
aux_z = 0# auxiliar da variavel z para append
j = 0 # contador de nivel
nivel = 1 # incializa variavel nivel
controle_nivel = 0 #controle de nivel
cont = 0
angle = 0 # angulo entre pontos
comp = [] # Vetor de comparacao entre variaveis
ponto_z = 0

def callback(data):
	global i
	global j
	global vetx
	global vety
	global vetz
	global cont
	global controle_nivel
	global nivel
	#np.append(aux_x,3)
	for i in range (0,len(data.points)):
#	while i< len(data.points):
			aux_x  = float(data.points[i].x)#Pega os valores dos pontos
			vetx.append(aux_x)
			aux_y = float(data.points[i].y)
			vety.append(aux_y)
			aux_z = float(data.points[i].z)
			vetz.append(aux_z)
	#		if vetz[i] > 0.175:
	#			vetz[i] = vetz[i] -0.175
	#		if vetz[i] < -0.175:
	#			vetz[i] = vetz[i] +0.175
			sum_root = (vetx[i]**2 + vety[i]**2 + vetz[i]**2)**0.5
			if j >15:	# Controle de nivel dos 16 ponto em sequencia para varredura
				nivel = nivel +1
				j = 0
			if  sum_root>1.0 and sum_root<2.0 or cont == 1: #identifica colisao
				#print "Indice de colisao ", i
				#print sum_root
				if sum_root != 0.0 :
					comp.append(sum_root)
				if len(comp) == 2:
					ponto_z =  len(vetz) - 1
					angle  = atan2(vetz[ponto_z],(comp[1]-comp[0]))
					comp.pop(0)
					angle = degrees(angle)
					if angle >= 30 and angle != 180:
						print angle
				controle_nivel = (nivel*16) -1
				#Inserir variavel para checar pontos de colisao
				if i<(controle_nivel):
					cont = 1
				if i == (controle_nivel):
					cont = 0
					print "\n"

			#Incrimento de J para controle de nivel
			j = j+1
			#Fim do loop zero os pontos
			i = i+1
			if i ==len(data.points):
				i = 0
				nivel = 0
				vetx=[]
				vety=[]
				vetz=[]
def getdata():
	    rospy.init_node("get_pointcloud",anonymous = True)
	    rospy.Subscriber("/velodyne_points",PointCloud,callback)
	    rate = rospy.Rate(20)
	    while not rospy.is_shutdown():
	            rate.sleep

if __name__== '__main__':
	try:
		getdata()
	except rospy.ROSInterruptException:
		pass
