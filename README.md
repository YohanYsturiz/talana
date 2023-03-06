#### Game JRPG Talana

#### Instalacion

1. Crear un entorno virtual con pyenv virtualenv utilizando python 3.11.1
2. Instalar los paquetes para la ejecucion del servicio `pip install -r requeriments.txt`
3. ejecutar el archivo kombat.py `python kombat.py`


### Respuestas a prueba teorica

1. Supongamos que en un repositorio GIT hiciste un commit y olvidaste un archivo. Explica cómo se
soluciona si hiciste push, y cómo si aún no hiciste.

    R: Si ya hemos hecho *push* entonces podemos agregar el archivo faltante haciendo otro commit y luego ejecutamos `git push --force` para forzar la actualizacion del repositorio remoto. 

    no es muy recomendable usar el `git push --force` si otras personas trabajan con el mismo repositorio, es importante comunicar que se ha realizado ese cambio.

    en caso de aun no hacer el *push* entonces agregamos el archivo que falta y utilizamos el comando `git commit --amend` para agregar ese cambio al ultimo commit, este comando permite cambios el mensaje del commit y luego solo sube los cambios con `git push`

2. Si has trabajado con control de versiones ¿Cuáles han sido los flujos con los que has trabajado?

    Si, en trabajado con git.

    y el flujo que mas he utilizado es un flujo basado en ramas y haciendo solicitudes de extraccion (pull-request), pero creando una rama partiendo de master para desarrollar el nuevo fix o funcionalidad luego de terminar el desarrollo se pasa una solicitud con la de QA se valida el codigo antes de aprobar el merge y luego de probar en QA se pasa a PROD.

3. ¿Cuál ha sido la situación más compleja que has tenido con esto?
    
    R:  Trabajando en un monolito teniamos problemas con las migraciones generadas ya que teniamos conflictos por la secuencia de las mismas, una de las soluciones fue ir separando el monolito en distintos microservicios y evitar la creacion de migraciones en el monolito. 

4. ¿Qué experiencia has tenido con los microservicios?

    R: He trabajado en la creacion y mantenimiento de microservicios con Python usando frameworks como Flask, FastApi y Django y algunos en PHP con Laravel. 

5. ¿Cuál es tu servicio favorito de GCP o AWS? ¿Por qué?

    R: Mi favorito es AWS, he trabajo con distintos servicios de AWS como s3, Lambdas, Steps Functions, Elastic Beanstalk, Databases y EC2.

