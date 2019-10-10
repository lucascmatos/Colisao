#!/usr/bin/env python
import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
import numpy

angMax=0
angMin=0
count=0
vet = []
global i 

def callback(data):
   global vet
   vet = list(data.ranges) #Pega as distancias medidas do topico
def deteccao_colisao():
   global check
   rospy.init_node("dados_laser",anonymous = True)#incia no do pacote
   rospy.Subscriber("/scan",LaserScan,callback)#subscreve no no do laser
   rate = rospy.Rate(1)
   f = open("/home/l/fora_colisa.txt","w")
   d = open("/home/l/dentro_colisa.txt","w")
   while not rospy.is_shutdown():
      for i in range(len(vet)): #Varre o vetor de pontos
         f.write("%s\n" %vet[i])
         if 0.03<vet[i]<1.0: #Checa se os pontos entao no meu range de colisao
            d.write("%s\n" %vet[i])
            print "Colisao"# se estiverem manda a mensagem de colisao
            #else:
            #       print "Nao vai bater"
   rate.sleep

                
if __name__== '__main__':
	try:
		deteccao_colisao()
	except rospy.ROSInterruptException:
		pass
