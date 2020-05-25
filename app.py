### para algoritmo
import streamlit as st
from PIL import Image
import pandas as pd
from pandas import DataFrame
import json
from firebase import firebase
import datetime
from datetime import datetime
from datetime import date
import base64
import os
os.environ['NUMEXPR_MAX_THREADS'] = '16'
##########################################################
#######[1]FILTROS DE BSQUEDA
##########################################################

image = Image.open('logo.jpg')
st.sidebar.image(image, caption='',use_column_width=True)

image = Image.open('banner.jpg')
st.image(image, caption='',use_column_width=True)

st.sidebar.title('BUSQUEDA FILTROS')
date_inicio = st.sidebar.date_input('Fecha inicio', datetime.today())
date_fin = st.sidebar.date_input('Fecha fin', datetime.today())
#educacion = st.sidebar.selectbox(label="Nivel educacion",options=["Universitaria", "Técnica", "Secundaria"],index=0,)


##########################################################
#######[2]CREAR PERFIL
##########################################################
st.sidebar.title('GENERAR PERFIL')
edad = st.sidebar.radio(label="Grupo Edad",options=['[18-22]','[23-37]','[38-58]','[59-73]','[74-mas]'],index=0,)
grado = st.sidebar.selectbox(label="Grado Formacion",options=['secundaria','tecnica','universitaria'])
estado = st.sidebar.selectbox(label="Estado Estudios",options=['completa','en curso','tuve que dejarlo'])
rubro = st.sidebar.selectbox(label="Rubro carrera",options=['negocios','humanidades','ingenieria','tecnologia','otros','secundaria'])
ec = st.sidebar.selectbox(label="Experiencia call",options=['Si','No'],index=0,)
eo = st.sidebar.selectbox(label="Otras experiencias",options=['Si','No'],index=0,)
se = st.sidebar.selectbox(label="Sin experiencia",options=['Si','No'],index=0,)
tipo = st.sidebar.selectbox(label="Tipo de experiencia",options=['Atencion','Ventas','Back office','Redes sociales'], index=0,)
tiempo = st.sidebar.radio(label="Tiempo de experiencia",options=['[0-3]','[4-6]','[7-12]','[12-mas]'],index=0,)


##########################################################
#######[3]CREAR SCORE DEL PERFIL BUSCADO
##########################################################

###################edad
if edad =='[18-22]':
	edad= 5      
if edad =='[23-37]':
	edad= 4
if edad =='[38-58]':
	edad= 3
if edad =='[59-73]':
	edad= 2	
if edad =='[74-mas]':
	edad= 1

Edad=edad

###################formacion
if grado =='secundaria':
	grado= 1      
if grado =='tecnica':
	grado= 2
if grado =='universitaria':
	grado= 3

grado_formacion=grado

###################estado estudios
if estado =='completa':
	estado= 3      
if estado =='en curso':
	estado= 2
if estado =='tuve que dejarlo':
	estado= 1

estado_estudios=estado

###################rubro de carrera
if rubro =='negocios':
	rubro= 4      
if rubro =='humanidades':
	rubro= 3
if rubro =='ingenieria':
	rubro= 2
if rubro =='tecnologia':
	rubro= 2	
if rubro =='otros':
	rubro= 1
if rubro =='secundaria':
	rubro= 1

rubro_carrera=rubro

###################experiencia call
if ec== 'Si': 
   Exp_call=5
else:
   Exp_call=0 

###################experiencia otros
if eo== 'Si': 
   Exp_otros=3
else:
   Exp_otros=0 

###################sin experiencia
if se== 'Si': 
   Sin_Exp=1
else:
   Sin_Exp=0 

###################tipo de experiencia
if tipo== 'Atencion': 
    ATC=1
    Ventas=0
    BO=0
    RS=0

if tipo== 'Ventas': 
    ATC=0
    Ventas=1
    BO=0
    RS=0

if tipo== 'Back office': 
    ATC=0
    Ventas=0
    BO=1
    RS=0

if tipo== 'Redes sociales': 
    ATC=0
    Ventas=0
    BO=0
    RS=1

###################tipo de experiencia
if tiempo =='[0-3]':
	tiempo= 5      
if tiempo =='[4-6]':
	tiempo= 4
if tiempo =='[7-12]':
	tiempo= 3
if tiempo =='[13-mas]':
	tiempo= 1
Tiempo_experiencia=tiempo


a1=(Edad*0.15)
b1=((grado_formacion*estado_estudios*rubro_carrera)*0.25)
c1=((Sin_Exp+Exp_otros+Exp_call)*0.30)
d1=((Sin_Exp*ATC)+(Sin_Exp*Ventas)+(Sin_Exp*RS)+(Sin_Exp*BO) *0.05 + ((Exp_otros*ATC*Tiempo_experiencia)+(Exp_otros*Ventas*Tiempo_experiencia)+(Exp_otros*BO**Tiempo_experiencia)+(Exp_otros*RS*Tiempo_experiencia))*0.05 + ((Exp_call*ATC*Tiempo_experiencia)+(Exp_call*Ventas*Tiempo_experiencia)+(Exp_call*BO*Tiempo_experiencia)+(Exp_call*RS*Tiempo_experiencia))*0.20)

X=a1+b1+c1+d1
##st.write('Score postulante a buscar: %s' % round(X,2))

firebase = firebase.FirebaseApplication('https://konectase-522d7.firebaseio.com/', None)

##########################################################
#######[4]PREPROCESAMIENTO DE DATOS
##########################################################

@st.cache 
def PROCESAMIENTO_DATOS():
###TRAEMOS TABLAS EN JSON
	postulantes= firebase.get('/POSTULANTES', None)
	postulantes=json.dumps(postulantes)
	profesional= firebase.get('/DATOS_PROFESIONALES', None)
	profesional=json.dumps(profesional)
	experiencia= firebase.get('/DATOS_EXPERIENCIA', None)
	experiencia=json.dumps(experiencia)

###CONVERTIMOS JSON A DATAFRAME
	data_postulantes=json.loads(postulantes)
	dfpostulantes = DataFrame(data_postulantes).T
	###TABLA PROFESIONAL
	data_profesional=json.loads(profesional)
	dfprofesional = DataFrame(data_profesional).T
	###TABLA PROFESIONAL
	data_experiencia=json.loads(experiencia)
	dfexperiencia = DataFrame(data_experiencia).T

###TABLA POSTULANTES
	#-(1)Tomamos las columnas  que nos van a servir de la tabla
	df_Rpostulantes=DataFrame(dfpostulantes[['RegistradoDate','fecha_nac', 'numdoc','nombres','apellido_p','apellido_m','telefono','agended','state','estado_civil','genero','n_hijos']])
	#-(2)Convertimos fecha de nacimiento a valor datetime
	df_Rpostulantes['fecha_nac'] = df_Rpostulantes.fecha_nac.astype('datetime64[ns]') 
	#-(3)Extraemos la fecha de registro principal y convertimos fecha de registro a valor datetime
	df_Rpostulantes['FechaRegistro'] = df_Rpostulantes.RegistradoDate.str['date'].astype('datetime64[ns]')
	#-(4)Extraemos la hora de registroprincipal
	df_Rpostulantes['HoraRegistro'] = (df_Rpostulantes.RegistradoDate.str['hour'])
	#-(5)Obtenemos la fecha de hoy (analisis)
	df_Rpostulantes['Fechahoy'] =date.today() 
	#-(6)llevamos el indice a una columna que es el id unico de postulante
	df_Rpostulantes ['id_postulante']= df_Rpostulantes.index 
	#-(7)Reseteamos el valor de los indices
	df_Rpostulantes.reset_index(level=0, inplace=True)
	#-(8)Convertimos la fecha hoy a datetime
	df_Rpostulantes['Fechahoy'] = df_Rpostulantes.Fechahoy.astype('datetime64[ns]')
	#-(9)Calculamos la edad del postulante
	df_Rpostulantes['Edad']=((df_Rpostulantes['Fechahoy']- df_Rpostulantes['fecha_nac']).astype('timedelta64[Y]')).astype(int)

###TABLA PROFESIONAL
	#-(1) Tomamos las columnas que nos sirven para la tabla
	df_Rprofesional=DataFrame(dfprofesional[['id_postulante','grado_formacion', 'estado_estudios','rubro_carrera']])
	#-(1) Reseteamos los indices
	df_Rprofesional=df_Rprofesional.fillna('Secundaria') 
	df_Rprofesional.reset_index(level=0,inplace=True)

###TABLA EXPERIENCIA
	#-(1)Seleccionando columnas para los registros sin experiencia.
	sinexperiencia=DataFrame(dfexperiencia[['id_postulante','flag_se','se_p_ventas','se_p_backof','se_p_redes','se_p_atc']])
	#-(2)Le damos valores numericos a las respuestas de la pregunta de ventas
	sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('A',1)
	sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('B',1)
	sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('C',0)
	sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].replace('D',0)
	sinexperiencia['se_p_ventas']=sinexperiencia['se_p_ventas'].fillna(0)
	#-(3)Le damos valores numericos a las respuestas de la pregunta de atc
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('5',1)
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('4',1)
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('3',0)
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('2',0)
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].replace('1',0)
	sinexperiencia['se_p_atc']=sinexperiencia['se_p_atc'].fillna(0)
	#-(4)Le damos valores numericos a las respuestas de la pregunta de BO
	sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('A',1)
	sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('B',1)
	sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('C',0)
	sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].replace('D',0)
	sinexperiencia['se_p_backof']=sinexperiencia['se_p_backof'].fillna(0)
	#-(5)Le damos valores numericos a las respuestas de la pregunta de BO
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('A',1)
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('B',1)
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('C',0)
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('D',0)
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].replace('E',0)
	sinexperiencia['se_p_redes']=sinexperiencia['se_p_redes'].fillna(0)
	sinexperiencia=sinexperiencia[sinexperiencia['flag_se']=='1']
	#-(6)Le damos valor Int a flag_se
	sinexperiencia['flag_se']=sinexperiencia['flag_se'].astype(int)
	### OBTENEMOS LA TABLA SUMARIZADA DE EXPERIENCIA
	#-(1)Seleccionando columnas para los registros con experiencia call.
	dataprev=DataFrame(dfexperiencia[['id_postulante','flag_ec','ec_segmento','ec_tiempo_exp']])
	#-(2) Filtramos los datos que tienen experiencia en call
	dataprev= dataprev[dataprev['flag_ec']==1]


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------///////////////////////////////////////////////////////////////////////////////////////////LIMPIEZA DE DATOS(ELIMINAR CUANDO EL PROCESO ESTE CORRECTO)
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("6m","6")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("1 m","1")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("5 m","5")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("3 m","3")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("7 m","7")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("9 m","9")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("8 m","8")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("2 a","24")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("1 a","12")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("3 a","36")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("6 m","36")
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].replace("1 y","12")
	dataprev['ec_tiempo_exp'] = dataprev['ec_tiempo_exp'] .fillna(0)
#----------///////////////////////////////////////////////////////////////////////////////////////////LIMPIEZA DE DATOS(ELIMINAR CUANDO EL PROCESO ESTE CORRECTO)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


	#-(3) La variable tiempo de experiencia en call la convertimos en entera (numerica)
	dataprev['ec_tiempo_exp']=dataprev['ec_tiempo_exp'].astype(int)
	dataprev['flag_ec']=dataprev['flag_ec'].astype(int)
	#-(4) hacemos un pivot de la tabla para obtener la sumatoria de la experiencia por cada segmento.
	dataprev2=dataprev.pivot_table(index='id_postulante', columns='ec_segmento', values=('ec_tiempo_exp'), aggfunc='sum').fillna(0) 
	#-(5) Renombramos las columnas de la tabla pivoteada. 
	dataprev2.rename(columns={'Atención al cliente':'qec_ATC','Ventas':'qec_Ventas','Back Office':'qec_BO','Crosseling':'qec_Cross','Redes Sociales':'qec_RS'},inplace=True)
	### OBTENEMOS LA TABLA SUMARIZADA DE LOS SEGMENTOS A LOS CUALES HA ATENDIDO
	#-(6) Generamos una tabla dummies con todos los segmentos
	dummies= pd.get_dummies(dataprev['ec_segmento']) 
	#-(7)tomamos de la tabla inicial dataprev  solo el Id del postulante para unirla con la tabla dummies que no tiene ID, servira en el siguiente paso.
	Rev=DataFrame(dataprev[['id_postulante','flag_ec']])
	#-(8) Cruzamos la tabla REV con dummies para obtener la llave.el cruce se hace con los indices
	union=pd.merge(Rev,dummies,left_index=True,right_index=True)
	#-(9) Renombramos las columnas de esta tabla denominada union.
	union.rename(columns={'Atención al cliente':'ec_ATC','Ventas':'ec_Ventas','Back Office':'ec_BO','Crosseling':'ec_Cross','Redes Sociales':'ec_RS'},inplace=True)
	#-(10) Generamos un pivot con esta tabla union para obtener por cada ID los segmentos en los cuales ha tenido experiencia.
	union2=union.pivot_table(index='id_postulante', values=('flag_ec','ec_ATC','ec_Ventas','ec_BO','ec_Cross','ec_RS'), aggfunc='sum').fillna(0) 
	### CRUCE DE TABLAS.
	#-(11) se hace un join entre el sumarizado de experiencia y el sumarizado de segmento.
	conexperienciacall=pd.merge(union2, dataprev2,left_on='id_postulante',right_on='id_postulante')
	### OBTENEMOS LA TABLA SUMARIZADA DE EXPERIENCIA
	#-(1)Seleccionando columnas para los registros con experiencia call.
	datapreveo=DataFrame(dfexperiencia[['id_postulante','flag_eo','eo_puesto','eo_tiempo_exp']])
	#-(2) Filtramos los datos que tienen experiencia en call
	datapreveo= datapreveo[datapreveo['flag_eo']==1]

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------///////////////////////////////////////////////////////////////////////////////////////////LIMPIEZA DE DATOS(ELIMINAR CUANDO EL PROCESO ESTE CORRECTO)
	datapreveo['eo_tiempo_exp']=datapreveo['eo_tiempo_exp'].replace("año","12")
	datapreveo['eo_tiempo_exp']=datapreveo['eo_tiempo_exp'].fillna(0) 
	datapreveo['eo_tiempo_exp']=datapreveo['eo_tiempo_exp'].fillna(0) 
#----------///////////////////////////////////////////////////////////////////////////////////////////LIMPIEZA DE DATOS(ELIMINAR CUANDO EL PROCESO ESTE CORRECTO)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

	datapreveo['flag_eo']=datapreveo['flag_eo'].astype(int)
	datapreveo['eo_tiempo_exp']=datapreveo['eo_tiempo_exp'].astype(int)
	#-(3)Categorizamos los puestos de acuerdo a los segmentos del call
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Atención al cliente','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Ventas','eo_Ventas')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Impulsador de productos','eo_Ventas')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Cajero','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Reponedor','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Almacén, Distribución y Reparto','eo_BO')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Soporte Técnico','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Atención en Salud','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Administrativo y Tramites','eo_BO')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Servicio de Transporte','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Operario','eo_BO')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Profesor','eo_Ventas')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Desarrollo de contenido(audiovisual, escrito, edición)','eo_RS')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Community Manager y Redes Sociales','eo_RS')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Asistente','eo_BO')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Secretaria','eo_ATC')
	datapreveo['eo_puesto']=datapreveo['eo_puesto'].replace('Otros','eo_ATC')

	#-(4) hacemos un pivot de la tabla para obtener la sumatoria de la experiencia por cada segmento.
	datapreveo2=datapreveo.pivot_table(index='id_postulante', columns='eo_puesto', values='eo_tiempo_exp', aggfunc='sum').fillna(0) 
	#-(5) Renombramos las columnas de la tabla pivoteada. 
	datapreveo2.rename(columns={'eo_ATC':'qeo_ATC','eo_Ventas':'qeo_Ventas','eo_BO':'qeo_BO','eo_RS':'qeo_RS'},inplace=True)
	### OBTENEMOS LA TABLA SUMARIZADA DE LOS SEGMENTOS A LOS CUALES HA ATENDIDO
	#-(6) Generamos una tabla dummies con todos los segmentos
	dummies2= pd.get_dummies(datapreveo['eo_puesto']) 
	#-(7)tomamos de la tabla inicial datapreveo  solo el Id del postulante para unirla con la tabla dummies que no tiene ID, servira en el siguiente paso.
	Rev2=DataFrame(datapreveo[['id_postulante','flag_eo']])
	#-(8) Cruzamos la tabla REV2 con dummies2 para obtener la llave.el cruce se hace con los indices
	unioneo=pd.merge(Rev2,dummies2,left_index=True,right_index=True)
	#-(9) Generamos un pivot con esta tabla unioneo para obtener por cada ID los segmentos en los cuales ha tenido experiencia.
	unioneo=unioneo.pivot_table(index='id_postulante', values=('flag_eo','eo_ATC','eo_Ventas','eo_BO','eo_RS'), aggfunc='sum').fillna(0) 
	### CRUCE DE TABLAS.
	#-(10) se hace un join entre el sumarizado de experiencia y el sumarizado de segmento.
	conexperienciaotros=pd.merge(unioneo, datapreveo2,left_on='id_postulante',right_on='id_postulante')


###TABLONPERFIL
	#-(0) Cruzamos la tabla postulantes con la experiencia call 
	tablonperfil=pd.merge(df_Rpostulantes, df_Rprofesional,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
	#-(1) Cruzamos la tabla postulantes con la experiencia call 
	tablonperfil=pd.merge(tablonperfil, conexperienciacall,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
	#-(2) Cruzamos la tabla postulantes con la experiencia otros
	tablonperfil=pd.merge(tablonperfil, conexperienciaotros,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
	#-(3) Cruzamos la tabla postulantes con la experiencia otros
	tablonperfil=pd.merge(tablonperfil, sinexperiencia,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
	#-(4)Seleccionando columnas necesarias para el analisis
	tablonperfil=DataFrame(tablonperfil[['id_postulante','numdoc','FechaRegistro','HoraRegistro','Fechahoy','Edad','grado_formacion','estado_estudios','rubro_carrera','nombres','apellido_p','apellido_m','telefono','agended','state',
	                                     'flag_se','flag_ec','flag_eo','ec_ATC','ec_BO','ec_Cross','ec_RS','ec_Ventas','qec_ATC','qec_BO','qec_Cross','qec_RS','qec_Ventas',
	                                     'eo_ATC','eo_BO','eo_RS','eo_Ventas','qeo_ATC','qeo_BO','qeo_RS','qeo_Ventas',
	                                     'se_p_ventas','se_p_backof','se_p_redes','se_p_atc','estado_civil','genero','n_hijos']])

	tablonperfil2=DataFrame(tablonperfil[['id_postulante','numdoc','FechaRegistro','HoraRegistro','Fechahoy','Edad','grado_formacion','estado_estudios','rubro_carrera','nombres','apellido_p','apellido_m','telefono','agended','state',
	                                     'flag_se','flag_ec','flag_eo','ec_ATC','ec_BO','ec_Cross','ec_RS','ec_Ventas','qec_ATC','qec_BO','qec_Cross','qec_RS','qec_Ventas',
	                                     'eo_ATC','eo_BO','eo_RS','eo_Ventas','qeo_ATC','qeo_BO','qeo_RS','qeo_Ventas',
	                                     'se_p_ventas','se_p_backof','se_p_redes','se_p_atc','estado_civil','genero','n_hijos']])

	#-(5)La columna edad convertirla a categorias
	bins=[-1,17,22,37,58,73,100]
	names=['[0-17]','[18-22]','[23-37]','[38-58]','[59-73]','[74-100]']
	tablonperfil['Edad']=pd.cut(tablonperfil['Edad'],bins,labels=names)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[0-17]',1)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[18-22]',5)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[23-37]',4)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[38-58]',3)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[59-73]',2)
	tablonperfil['Edad']=tablonperfil['Edad'].replace('[74-100]',1)
	#-(6)grado de formacion en valor numerico
	tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Secundaria',1)
	tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Técnica',2)
	tablonperfil['grado_formacion']=tablonperfil['grado_formacion'].replace('Universitaria',3)
	#-(7)estado_estudios en valor numerico
	tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('Tuve que dejarlo',1)
	tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('En curso',2)
	tablonperfil['estado_estudios']=tablonperfil['estado_estudios'].replace('Completa',3)
	#-(8)las columnas flag que tengan un valor 1 si es mayor que 1.
	tablonperfil['flag_se']=tablonperfil['flag_se'].where(tablonperfil['flag_se']<2, 1)
	tablonperfil['flag_ec']=tablonperfil['flag_ec'].where(tablonperfil['flag_ec']<2, 1)
	tablonperfil['flag_eo']=tablonperfil['flag_eo'].where(tablonperfil['flag_eo']<2, 1)
	#-(8)experiencia call
	tablonperfil['ec_ATC']=tablonperfil['ec_ATC'].where(tablonperfil['ec_ATC']<2, 1)
	tablonperfil['ec_BO']=tablonperfil['ec_BO'].where(tablonperfil['ec_BO']<2, 1)
	tablonperfil['ec_Cross']=tablonperfil['ec_Cross'].where(tablonperfil['ec_Cross']<2, 1)
	tablonperfil['ec_RS']=tablonperfil['ec_RS'].where(tablonperfil['ec_RS']<2, 1)
	tablonperfil['ec_Ventas']=tablonperfil['ec_Ventas'].where(tablonperfil['ec_Ventas']<2, 1)
	tablonperfil['eo_ATC']=tablonperfil['eo_ATC'].where(tablonperfil['eo_ATC']<2, 1)
	tablonperfil['eo_BO']=tablonperfil['eo_BO'].where(tablonperfil['eo_BO']<2, 1)
	tablonperfil['eo_RS']=tablonperfil['eo_RS'].where(tablonperfil['eo_RS']<2, 1)
	tablonperfil['eo_Ventas']=tablonperfil['eo_Ventas'].where(tablonperfil['eo_Ventas']<2, 1)
	#-(9)convertirmos rubro carrera en numerica
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Administración (Todas las afines). Ejemplo: Neg.Internacionales, bancaria,etc)',4)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Administración (Todas las afines)',4)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Economía, Contabilidad y Finanzas',4)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Redes Sociales',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Computación e Informática',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Derecho y Ciencias Políticas',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Psicología',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Sistemas',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Industrial, Ambiental, Estadística',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Diseño (Gráfico, Publicitario o Web)',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Medicina, Enfermeria, Farmacia o Fisioterapia)',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ciencia de la Comunicación',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Educación',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Secretariado',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Turismo y Aviación Comercial',4)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Idiomas',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Gastronomía y Repostería',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing.Civil, Arquitectura, Diseño de Interiores',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Literatura, Historia, Filosofía, Sociología',3)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing. Electrónica / Electricidad',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Ing.Agricola o Química',3) 
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Otros',2)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].replace('Secundaria',1)
	tablonperfil['rubro_carrera']=tablonperfil['rubro_carrera'].astype(int)
	#-(10)La columna qexperiencia call convertirla a categorias
	bins2=[-1,3,6,12,500]
	names2=['[0-3]','[3-6]','[6-12]','[12-mas]']
	tablonperfil['qec_ATC']=pd.cut(tablonperfil['qec_ATC'],bins2,labels=names2)
	tablonperfil['qec_BO']=pd.cut(tablonperfil['qec_BO'],bins2,labels=names2)
	tablonperfil['qec_Cross']=pd.cut(tablonperfil['qec_Cross'],bins2,labels=names2)
	tablonperfil['qec_RS']=pd.cut(tablonperfil['qec_RS'],bins2,labels=names2)
	tablonperfil['qec_Ventas']=pd.cut(tablonperfil['qec_Ventas'],bins2,labels=names2)
	tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[0-3]',1)
	tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[3-6]',2)
	tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[6-12]',3)
	tablonperfil['qec_ATC']=tablonperfil['qec_ATC'].replace('[12-mas]',4)
	tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[0-3]',1)
	tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[3-6]',2)
	tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[6-12]',3)
	tablonperfil['qec_BO']=tablonperfil['qec_BO'].replace('[12-mas]',4)
	tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[0-3]',1)
	tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[3-6]',2)
	tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[6-12]',3)
	tablonperfil['qec_Cross']=tablonperfil['qec_Cross'].replace('[12-mas]',4)
	tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[0-3]',1)
	tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[3-6]',2)
	tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[6-12]',3)
	tablonperfil['qec_RS']=tablonperfil['qec_RS'].replace('[12-mas]',4)
	tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[0-3]',1)
	tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[3-6]',2)
	tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[6-12]',3)
	tablonperfil['qec_Ventas']=tablonperfil['qec_Ventas'].replace('[12-mas]',4)
	#-(11)La columna qexperiencia otros convertirla a categorias
	tablonperfil['qeo_ATC']=pd.cut(tablonperfil['qeo_ATC'],bins2,labels=names2)
	tablonperfil['qeo_BO']=pd.cut(tablonperfil['qeo_BO'],bins2,labels=names2)
	tablonperfil['qeo_RS']=pd.cut(tablonperfil['qeo_RS'],bins2,labels=names2)
	tablonperfil['qeo_Ventas']=pd.cut(tablonperfil['qeo_Ventas'],bins2,labels=names2)
	tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[0-3]',1)
	tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[3-6]',2)
	tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[6-12]',3)
	tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].replace('[12-mas]',4)
	tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[0-3]',1)
	tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[3-6]',2)
	tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[6-12]',3)
	tablonperfil['qeo_BO']=tablonperfil['qeo_BO'].replace('[12-mas]',4)
	tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[0-3]',1)
	tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[3-6]',2)
	tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[6-12]',3)
	tablonperfil['qeo_RS']=tablonperfil['qeo_RS'].replace('[12-mas]',4)
	tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[0-3]',1)
	tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[3-6]',2)
	tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[6-12]',3)
	tablonperfil['qeo_Ventas']=tablonperfil['qeo_Ventas'].replace('[12-mas]',4)
	tablonperfil['qeo_ATC']=tablonperfil['qeo_ATC'].fillna(0) 
	#---------------------------------------------------------------------------------
	#-(12)agrupar en dos los datos de la sin experiencia(clasificaciones)
	#tablonperfil['se_p_ventas']=tablonperfil['se_p_ventas'].replace(0,1)
	#tablonperfil['se_p_ventas']=tablonperfil['se_p_ventas'].replace(0,1)
	#---------------------------------------------------------------------------------
	#-(13)cambiar el impacto de la experiencia
	tablonperfil['flag_ec']=tablonperfil['flag_ec'].replace(1,5)
	tablonperfil['flag_eo']=tablonperfil['flag_eo'].replace(1,3)
	tablonperfil['flag_se']=tablonperfil['flag_se'].replace(1,1)
	# ## **PASO 4**:* Ejecución de algoritmo* 
	tablonperfil['qec_Ventas']= tablonperfil['qec_Ventas'].fillna(1)
	tablonperfil['qeo_RS']= tablonperfil['qeo_RS'].fillna(1)

##CALCULAR ALGORITMO ICP	
	a2=(tablonperfil['Edad'].astype(int)*0.15)
	b2=((tablonperfil['grado_formacion']*tablonperfil['estado_estudios']*tablonperfil['rubro_carrera'])*0.25)  
	c2=((tablonperfil['flag_se']+tablonperfil['flag_eo']+ tablonperfil['flag_ec'])*0.30)
	d2=((tablonperfil['flag_se'].astype(int)*tablonperfil['se_p_atc'].astype(int) + tablonperfil['flag_se'].astype(int)*tablonperfil['se_p_ventas'].astype(int) + tablonperfil['flag_se'].astype(int)*tablonperfil['se_p_redes'].astype(int) + tablonperfil['flag_se'].astype(int)*tablonperfil['se_p_backof'].astype(int))*0.05 + ((tablonperfil['flag_eo'].astype(int)*tablonperfil['eo_ATC'].astype(int)*tablonperfil['qeo_ATC'].astype(int) + tablonperfil['flag_eo'].astype(int)*tablonperfil['eo_Ventas'].astype(int)*tablonperfil['qeo_Ventas'].astype(int) + tablonperfil['flag_eo'].astype(int)*tablonperfil['eo_BO'].astype(int)*tablonperfil['qeo_BO'].astype(int) + tablonperfil['flag_eo'].astype(int)*tablonperfil['eo_RS'].astype(int)*tablonperfil['qeo_RS'].astype(int))*0.05) + ((tablonperfil['flag_ec'].astype(int)*tablonperfil['ec_ATC'].astype(int)*tablonperfil['qec_ATC'].astype(int) + tablonperfil['flag_ec'].astype(int)*tablonperfil['ec_Ventas'].astype(int)*tablonperfil['qec_Ventas'].astype(int) + tablonperfil['flag_ec'].astype(int)*tablonperfil['ec_BO'].astype(int)*tablonperfil['qec_BO'].astype(int) + tablonperfil['flag_ec'].astype(int)*tablonperfil['ec_RS'].astype(int)*tablonperfil['qec_RS'].astype(int))*0.20))
	Y=a2+b2+c2+d2
	Z=DataFrame(round(abs((Y-X)/X)*100))
	Z.columns = ['ICP']
	# ## **PASO 5**:* Revisión de tabla final* 
	final=pd.merge(tablonperfil2,Z,left_index=True,right_index=True)
	final = final[(final['FechaRegistro'] >= pd.Timestamp(date_inicio)) & (final['FechaRegistro'] <= pd.Timestamp(date_fin))]
	
##CALCULAR SUELDO Y VARIABLES
	Calulosueldo=DataFrame(dfexperiencia[['id_postulante','eo_retribucion_basico', 'ec_retribucion_basico']])
	Calulosueldo=Calulosueldo.fillna(0)
	Calulosueldo['eo_retribucion_basico']=Calulosueldo['eo_retribucion_basico'].replace(0,900)
	Calulosueldo['eo_retribucion_basico']=Calulosueldo['eo_retribucion_basico'].replace("N/A",900)
	Calulosueldo['eo_retribucion_basico']=Calulosueldo['eo_retribucion_basico'].replace("O",900)
	Calulosueldo['eo_retribucion_basico']=Calulosueldo['eo_retribucion_basico'].replace("5.00",500)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace(0,900)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('000',900)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('0000',900)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('1',900)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('8 50',900)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('-930',930)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('-9340',930)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('85o',850)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].replace('900.00',850)
	Calulosueldo['eo_retribucion_basico']=Calulosueldo['eo_retribucion_basico'].astype(int)
	Calulosueldo['ec_retribucion_basico']=Calulosueldo['ec_retribucion_basico'].astype(int)
	eo=pd.DataFrame(Calulosueldo.groupby(['id_postulante'])['eo_retribucion_basico'].mean())
	ec=pd.DataFrame(Calulosueldo.groupby(['id_postulante'])['ec_retribucion_basico'].mean())
	sueldo=pd.merge(eo, ec,left_on='id_postulante',right_on='id_postulante',how='left').fillna(0) 
	sueldo['sueldo']=(sueldo['eo_retribucion_basico'] + sueldo['ec_retribucion_basico'])/2
	bins5=[-1,900,1000,1300,10000]
	names5=[1,2,3,4]
	sueldo['sueldo2']=pd.cut(sueldo['sueldo'],bins5,labels=names5)
	rotacion=DataFrame(tablonperfil[[ 'id_postulante','numdoc','Edad','grado_formacion','estado_estudios','estado_civil','genero','n_hijos']])
	rotacion=pd.merge(rotacion, sueldo,left_on='id_postulante',right_on='id_postulante',how='left') 
	rotacion['sueldo2']=rotacion['sueldo2'].fillna(1).astype(int)
	#---coeficientes de edad
	bins=[-1,17,22,37,58,73,100]
	names=[0,5,4,3,2,1]
	rotacion['Edad']=pd.cut(rotacion['Edad'],bins,labels=names)
	rotacion['Edad']=rotacion['Edad'].astype(int)
	rotacion['Edad']=rotacion['Edad'].replace(1,-1.20654*2)
	rotacion['Edad']=rotacion['Edad'].replace(2,-1.20654*2)
	rotacion['Edad']=rotacion['Edad'].replace(3,-2.75857*3)
	rotacion['Edad']=rotacion['Edad'].replace(4,0.953878*4)
	rotacion['Edad']=rotacion['Edad'].replace(5,1.68204 *5)
	#---coeficientes de grado de formacion
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace(0,-0.51932*1)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace(1,-0.51932*1)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace(2,-0.470772*2)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace(3,-0.339102*3)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace('Universitaria',-0.339102*3)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace('Técnica',-0.470772*2)
	rotacion['grado_formacion']=rotacion['grado_formacion'].replace('Secundaria',-0.51932*1)
	rotacion['grado_formacion']=rotacion['grado_formacion'].astype(float)
	#---coeficientes de estado de estudios
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace(0,-0.552312*1)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace(1,-0.552312*1)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace(2,-0.220668*2)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace(3,-0.556213*3)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace('Tuve que dejarlo',-0.552312*1)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace('Completa',-0.556213*3)
	rotacion['estado_estudios']=rotacion['estado_estudios'].replace('En curso',-0.220668*2)
	rotacion['estado_estudios']=rotacion['estado_estudios'].astype(float)
	#---coeficientes de estado civil
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Soltero(a)',-0.713386*1)
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Conviviente',-0.615807*2)
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Casado(a)',-0.615807*2)
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Separado(a)',-0.713386*1)
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Divorciado(a)',-0.713386*1)
	rotacion['estado_civil']=rotacion['estado_civil'].replace('Viudo(a)',-0.713386*1)
	rotacion['estado_civil']=rotacion['estado_civil'].replace(0,-0.621284*1)
	#---coeficientes de genero
	rotacion['genero']=rotacion['genero'].replace('Femenino',-0.612034*1)
	rotacion['genero']=rotacion['genero'].replace('Masculino',-0.717159*2)
	rotacion['genero']=rotacion['genero'].replace('Prefiero no responder',-0.612034*1)
	#---coeficientes de hijos
	rotacion['n_hijos']=rotacion['n_hijos'].replace(-2,2)
	rotacion['n_hijos']=rotacion['n_hijos'].replace('no',0)
	rotacion['n_hijos']=rotacion['n_hijos'].replace('Hefdf',0)
	rotacion['n_hijos']=rotacion['n_hijos'].replace('No',0)
	rotacion['n_hijos']=rotacion['n_hijos'].replace(13,5)
	rotacion['n_hijos']=rotacion['n_hijos'].replace(8,5)
	rotacion['n_hijos']=rotacion['n_hijos']*-0.216554
	#---coeficientes de sueldo
	rotacion['sueldo2']=rotacion['sueldo2'].replace(1,2.22881*1)
	rotacion['sueldo2']=rotacion['sueldo2'].replace(2,-4.77661*2)
	rotacion['sueldo2']=rotacion['sueldo2'].replace(3,3.23339*3)
	rotacion['sueldo2']=rotacion['sueldo2'].replace(4,-2.01478*4)

##CALCULO ICR
	numerador=2.71828**(-1.32919+rotacion['Edad']+rotacion['grado_formacion']+rotacion['estado_estudios']+rotacion['estado_civil']+rotacion['estado_civil']+rotacion['n_hijos']+rotacion['sueldo2'])
	denominador=1+2.71828**(-1.32919+rotacion['Edad']+rotacion['grado_formacion']+rotacion['estado_estudios']+rotacion['estado_civil']+rotacion['estado_civil']+rotacion['n_hijos']+rotacion['sueldo2'])

	rotacion['IPR']=round(numerador.astype(float)/denominador.astype(float),4)
	rotacionfinal=DataFrame(rotacion[[ 'id_postulante','sueldo','IPR']])

##CALCULO FINAL FINAL - AHORA SI
	Final_Final_2=pd.merge(final,rotacionfinal,left_on='id_postulante',right_on='id_postulante',how='left')
	Final_Final_2=DataFrame(Final_Final_2[[ 'id_postulante','numdoc','Edad','grado_formacion','estado_estudios','rubro_carrera','flag_ec','flag_eo','flag_se','estado_civil','genero','n_hijos','sueldo','ICP','IPR']])
	return(Final_Final_2)


html_temp = """
	<div style="background-color:#009688;opacity: 0.80;padding:0.9 px">
	<h2 style="color:white;text-align:left;">Determinar los índices de búsqueda</h2></div>
	"""
st.markdown(html_temp,unsafe_allow_html=True)
#st.title('DETERMINAR SCORE DE BUSQUEDA')
st.write('**ICP:Indice de correlación con el perfl**')
ICP = st.slider(label="Cercano a cero significa mayor relación",min_value=-0.0,max_value=100.0,value=100.0,step=1.0)
st.write('**IPR: Indice de probabilidad de rotacion temprana**')
IPR = st.slider(label="Cercano a cero significa menor rotación",min_value=-0.0,max_value=1.0,value=1.0,step=0.1)


#	final= final[final['Score'] <= score]
#	return(final)


##########################################################
#######[4]ALGORITMO
##########################################################


def main():
	html_temp = """
	<div style="background-color:#009688;opacity: 0.8;padding:0.9 px">
	<h2 style="color:white;text-align:left;">Ejecutar predicción</h2></div>
	"""
	st.markdown(html_temp,unsafe_allow_html=True)

	if st.button("Ejecutar"):
			result = PROCESAMIENTO_DATOS()
			result = result[result['ICP'] <= ICP]
			result = result[result['IPR'] <= IPR]
			result = result.sort_values(by=['ICP'])#, ascending=True)

			st.write('Grafico de dispersión: %s' % len(result))
			import altair as alt
			c = alt.Chart(result.loc[:, ['IPR','ICP','sueldo','genero']]).mark_circle().encode(
			x='IPR', y='ICP', size='sueldo', color='genero', tooltip=['IPR', 'ICP', 'sueldo','genero'])
			st.altair_chart(c, use_container_width=True)

			st.write('Cantidad de postulantes encontrados: %s' % len(result))

			#cols = ['id_postulante','numdoc','Edad','grado_formacion','estado_estudios','rubro_carrera','flag_ec','flag_eo','flag_se','estado_civil','genero','n_hijos','sueldo','ICP','IPR']
			#st_ms = st.multiselect("Columns", list(result.index), ['id_postulante','ICP','IPR'])
			#result = result.loc[st_ms]
			st.dataframe(result)

			df = pd.DataFrame(result)
			csv = df.to_csv(index=False)
			b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
			href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
			st.markdown(href, unsafe_allow_html=True)


if __name__ == '__main__':
	main()


st.text("-------------------------------------------------------------------------")
st.text("Laboratorio de ciencia de datos")
st.text("Konecta_Perú")  
###--ejecutar C:\Users\LENOVO\PROYECTO_ML_API_STREAMLIT_RRHH>streamlit run app.py
