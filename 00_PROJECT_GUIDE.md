# Asistente Inteligente para Planeación de Costos Operativos

> Estado del documento: 🟡 En construcción

---

# 0. Propósito del documento

**Estado:** 🟢 Aprobada

Este documento constituye la especificación funcional oficial del proyecto **Asistente Inteligente para Planeación de Costos Operativos**.

Su propósito es definir el producto que se está construyendo, documentar las decisiones arquitectónicas adoptadas durante el desarrollo y servir como referencia principal para comprender el alcance, las capacidades y la evolución del asistente.

A diferencia de los notebooks, cuyo objetivo es documentar el análisis de datos y garantizar la reproducibilidad técnica de los modelos desarrollados, este documento describe el producto de inteligencia artificial construido a partir de dichos análisis.

Este documento se considera la fuente oficial de definición del producto (Product Bible). Toda decisión funcional o arquitectónica que modifique el comportamiento del asistente deberá registrarse aquí antes de ser implementada.

A medida que el proyecto evolucione, este documento será actualizado para reflejar nuevas capacidades, herramientas, decisiones arquitectónicas y versiones del producto.

---
# 1. Definición del producto

**Estado:** 🟢 Aprobada

Esta sección define el producto desarrollado como resultado del caso de negocio. Su propósito es establecer qué es el asistente, el valor que aporta, a quién está dirigido y cuáles son los principales escenarios de uso que soporta dentro del alcance del MVP.

## 1.1 ¿Qué es el producto?
El **Asistente Inteligente para Planeación de Costos Operativos** es un sistema conversacional basado en inteligencia artificial diseñado para apoyar la estimación y el análisis de los costos de adquisición de equipos utilizados en proyectos de construcción.

El asistente integra el conocimiento obtenido durante el análisis de datos, los modelos de pronóstico desarrollados y herramientas de consulta para responder, en lenguaje natural, preguntas relacionadas con el comportamiento histórico de los precios y la proyección futura de los costos de los equipos.

Su propósito es transformar los resultados técnicos del análisis en información clara, útil y accionable, facilitando la consulta de tendencias, la interpretación de los resultados y la estimación de costos como apoyo a la planeación financiera de proyectos.

El producto ha sido diseñado bajo una arquitectura de agente de inteligencia artificial, permitiendo combinar diferentes fuentes de información y herramientas especializadas para generar respuestas fundamentadas según la intención de la consulta realizada por el usuario.

## 1.2 Valor que entrega
El Asistente Inteligente para Planeación de Costos Operativos proporciona una herramienta de apoyo para la toma de decisiones relacionadas con la adquisición de equipos en proyectos de construcción.

Su principal valor consiste en transformar datos históricos y resultados analíticos en información accesible mediante una interacción conversacional, permitiendo a los usuarios comprender el comportamiento de los costos y estimar su evolución futura sin necesidad de interpretar directamente modelos estadísticos o código.

A través de este producto es posible:

- Consultar el comportamiento histórico de los precios de materias primas y equipos.
- Obtener estimaciones del costo futuro de los equipos junto con su nivel de incertidumbre.
- Comprender las principales tendencias observadas durante el análisis.
- Disponer de un mecanismo reproducible para apoyar la planeación financiera de nuevas fases del proyecto.
- Complementar las estimaciones del modelo con información externa relevante del mercado, como noticias, tendencias económicas o variaciones en los precios de materias primas.

En conjunto, estas capacidades contribuyen a reducir la incertidumbre en la estimación de costos y proporcionan una base analítica que facilita la planificación y el seguimiento de los costos operativos.

## 1.3 Usuarios objetivo
El producto está dirigido a personas involucradas en la planeación, análisis y seguimiento de los costos operativos de proyectos de construcción, así como a usuarios que requieran consultar los resultados del análisis realizado.

Los principales usuarios identificados son:

- **Gerentes de proyecto**, interesados en anticipar el costo de adquisición de los equipos durante las diferentes fases del proyecto.
- **Responsables de planeación financiera**, quienes requieren estimaciones de costos para la elaboración y seguimiento de presupuestos.
- **Analistas de costos**, encargados de consultar el comportamiento histórico de los precios y apoyar la toma de decisiones mediante información analítica.
- **Evaluadores o interesados en el proyecto**, que deseen explorar los hallazgos del análisis, comprender las proyecciones realizadas y consultar los resultados obtenidos a través del agente conversacional.

El asistente ha sido diseñado para ofrecer respuestas en lenguaje natural, permitiendo que usuarios con distintos niveles de conocimiento técnico puedan acceder a la información de manera sencilla e intuitiva.

## 1.4 Casos de uso principales
Dentro del alcance del MVP, el Asistente Inteligente para Planeación de Costos Operativos permite a los usuarios realizar consultas relacionadas con el análisis histórico y la proyección de costos de los equipos mediante una interfaz conversacional.

Los principales casos de uso son:

- Consultar el comportamiento histórico de los precios de las materias primas y los equipos.
- Obtener el precio estimado de un equipo para una fecha futura dentro del horizonte de predicción definido.
- Conocer el rango de incertidumbre asociado a una predicción.
- Identificar tendencias históricas y proyectadas en los costos de los equipos.
- Consultar los principales hallazgos obtenidos durante el análisis de los datos.
- Comprender la influencia de las materias primas sobre el comportamiento de los costos de los equipos mediante explicaciones en lenguaje natural.
- Complementar las respuestas con información externa relevante del mercado, como noticias, tendencias económicas o variaciones en los precios de las materias primas, cuando esta se encuentre disponible.

Estos casos de uso constituyen la primera versión funcional del producto y podrán ampliarse en futuras iteraciones mediante la incorporación de nuevas herramientas, fuentes de información y capacidades analíticas.

---


# 2. Problema de negocio

**Estado:** 🟢 Aprobada

Esta sección describe el contexto empresarial que motiva el desarrollo del producto y define el problema que se busca resolver mediante el análisis de datos, los modelos predictivos y el asistente inteligente.

## 2.1 Contexto
Una empresa del sector construcción se encuentra en la etapa de planificación de un proyecto cuya ejecución requiere el suministro continuo de dos tipos de equipos críticos para las operaciones en campo.

El costo de adquisición de estos equipos ha presentado variaciones significativas a lo largo del tiempo, generando incertidumbre durante la planeación financiera y provocando desviaciones presupuestales en proyectos anteriores.

La empresa dispone de información histórica correspondiente a los precios de diferentes materias primas y de los equipos, con el propósito de identificar relaciones que permitan comprender el comportamiento de los costos y anticipar su evolución futura.


## 2.2 Problema identificado
La organización no cuenta con un mecanismo analítico que permita explicar qué materias primas influyen sobre el comportamiento de los costos de los equipos ni dispone de un modelo que permita estimar dichos costos de forma consistente para apoyar la planeación financiera.

Como consecuencia, las decisiones relacionadas con la adquisición de equipos se realizan bajo un alto nivel de incertidumbre, dificultando la elaboración de presupuestos y la gestión de los recursos del proyecto.

## 2.3 Objetivos del negocio
El proyecto busca proporcionar una metodología reproducible que permita:

- Comprender el comportamiento histórico de los costos de los equipos y de las materias primas asociadas.
- Identificar las variables con mayor influencia sobre el precio de cada equipo.
- Estimar el costo futuro de los equipos mediante modelos de pronóstico.
- Incorporar la incertidumbre propia de las estimaciones para apoyar una mejor interpretación de los resultados.
- Facilitar la consulta de los hallazgos mediante un asistente conversacional basado en inteligencia artificial.

## 2.4 Beneficios esperados
La solución propuesta busca aportar los siguientes beneficios al negocio:

- Anticipar los costos de adquisición de equipos antes del inicio de cada fase del proyecto.
- Reducir las desviaciones presupuestales asociadas a la volatilidad de los precios.
- Proporcionar una base analítica que apoye la planeación financiera y la toma de decisiones.
- Facilitar el acceso a los resultados del análisis mediante una interacción conversacional.
- Enriquecer las respuestas del asistente con información externa relevante del mercado cuando esta se encuentre disponible.

---

# 3. Alcance funcional del MVP

**Estado:** 🟢 Aprobada

Esta sección define las capacidades funcionales incluidas en la primera versión del producto (MVP). Su propósito es establecer claramente qué puede hacer el asistente, cuáles son sus principales capacidades conversacionales y cuáles son los límites de esta primera versión.

## 3.1 Misión
Permitir que los responsables de la planeación y análisis de costos operativos comprendan el comportamiento histórico de los precios y anticipen la evolución futura del costo de los equipos mediante una interacción conversacional basada en inteligencia artificial.

## 3.2 Capability Map
El MVP se construye sobre dos capacidades principales:

### Capacidad 1. Comprender el comportamiento histórico
Permite consultar, resumir e interpretar el comportamiento histórico de las materias primas y los equipos a partir de la información analizada durante el proyecto.

### Capacidad 2. Anticipar el comportamiento futuro
Permite estimar el costo futuro de los equipos utilizando los modelos predictivos desarrollados, comunicando la predicción junto con su nivel de incertidumbre.

## 3.3 Conversaciones del MVP
Durante esta primera versión el asistente será capaz de mantener conversaciones relacionadas con:

### Análisis histórico
- ¿Cómo se ha comportado el precio del Equipo 1?
- ¿Cuál ha sido la tendencia del Equipo 2?
- ¿Cómo evolucionó la materia prima Price_Y?
- ¿Qué comportamiento presentó determinada materia prima durante un período específico?
- ¿Cuáles fueron los principales hallazgos del análisis?

### Proyección de costos
- ¿Cuál será el precio estimado del Equipo 1 para una fecha determinada?
- ¿Cuál será el precio estimado del Equipo 2?
- ¿Cuál es el rango de incertidumbre de la predicción?
- ¿Qué tendencia se espera para los próximos meses?

### Contexto de negocio
- ¿Qué información analiza este asistente?
- ¿Qué equipos forman parte del estudio?
- ¿Cuál es el objetivo del proyecto?
- ¿Cómo puede utilizarse este asistente para apoyar la planeación financiera?

## 3.4 Capacidades técnicas
Para responder las consultas del usuario, el asistente podrá utilizar diferentes mecanismos según la naturaleza de la pregunta:

| Tipo de consulta | Fuente principal |
|------------------|------------------|
| Información del proyecto | Base de conocimiento |
| Hallazgos del análisis | Base de conocimiento |
| Consulta histórica | Herramientas de consulta sobre los datos históricos |
| Predicción de costos | Modelo de forecasting |
| Contexto de mercado | Información externa (cuando esté disponible) |

La selección del mecanismo adecuado será realizada automáticamente por el agente según la intención identificada en la consulta del usuario.

## 3.5 Restricciones del MVP
La primera versión del producto no contempla las siguientes capacidades:

- Realizar recomendaciones automáticas de compra.
- Sustituir el criterio de un analista financiero.
- Garantizar la exactitud de las predicciones.
- Explicar en detalle la metodología estadística utilizada para entrenar los modelos.
- Ejecutar análisis distintos a los contemplados en el alcance del proyecto.

Estas capacidades podrán incorporarse en versiones futuras del producto.

---

# 4. Arquitectura funcional

**Estado:** 🟢 Aprobada

Esta sección describe el funcionamiento general del Asistente Inteligente para Planeación de Costos Operativos desde una perspectiva funcional, mostrando cómo interactúan el usuario, el agente, las fuentes de conocimiento y las herramientas utilizadas para construir las respuestas.

## 4.1 Flujo general del asistente
El funcionamiento del asistente sigue un flujo orientado por la intención del usuario. Cada consulta es analizada para identificar el tipo de información requerida y seleccionar automáticamente la fuente más adecuada para construir la respuesta.

El resultado es una interacción conversacional que combina información documental, consultas sobre datos históricos, modelos predictivos y, cuando corresponda, conocimiento externo del mercado.

## 4.2 Componentes principales
La arquitectura funcional del MVP está compuesta por los siguientes componentes:

- **Usuario:** realiza consultas en lenguaje natural.
- **Agente de IA:** interpreta la intención de la consulta y coordina la obtención de la información necesaria.
- **Base de conocimiento:** almacena el conocimiento generado durante el análisis del proyecto y proporciona contexto para responder preguntas relacionadas con los hallazgos.
- **Herramientas especializadas:** permiten consultar información histórica, ejecutar modelos de pronóstico y acceder a otras capacidades específicas.
- **Fuentes externas de información:** suministran contexto adicional sobre tendencias del mercado, noticias o factores económicos cuando esta información se encuentre disponible.

## 4.3 Origen del conocimiento
El asistente obtiene la información utilizada para responder las consultas a partir de diferentes fuentes:

- Resultados obtenidos durante el análisis exploratorio y econométrico.
- Conclusiones derivadas del modelado predictivo.
- Series históricas de materias primas y equipos.
- Modelos de forecasting desarrollados para el proyecto.
- Información externa del mercado utilizada para complementar el análisis.

Cada fuente cumple una función específica dentro del proceso de generación de respuestas.

## 4.4 Uso de herramientas
El asistente utiliza herramientas especializadas para ejecutar tareas que requieren procesamiento adicional y que no pueden resolverse únicamente mediante recuperación de información.

Entre las principales herramientas del MVP se encuentran:

- Consulta de información histórica.
- Generación de pronósticos de costos.
- Consulta de la base de conocimiento.
- Recuperación de información externa relevante para complementar el contexto de una respuesta.

La selección de la herramienta adecuada depende de la intención identificada en la consulta realizada por el usuario.

## 4.5 Flujo de decisión del asistente
El proceso de atención de una consulta sigue el siguiente flujo funcional:

1. El usuario realiza una consulta en lenguaje natural.
2. El agente identifica la intención de la consulta.
3. Se determina la fuente de información más adecuada para responder.
4. Si es necesario, el agente ejecuta una o varias herramientas.
5. La información recuperada se integra en una respuesta única.
6. El asistente entrega una respuesta clara, fundamentada y adaptada al contexto del usuario.

Este flujo permite combinar diferentes fuentes de conocimiento dentro de una única interacción conversacional, proporcionando respuestas consistentes y orientadas al apoyo en la toma de decisiones.

---

# 5. Roadmap del producto

**Estado:** 🟢 Aprobada

Esta sección describe la evolución prevista del producto, estableciendo las capacidades incluidas en el MVP y las funcionalidades consideradas para versiones posteriores.

## MVP
La primera versión del producto tendrá como objetivo validar el funcionamiento del asistente y demostrar la integración entre el análisis de datos, los modelos predictivos y la inteligencia artificial conversacional.

Las capacidades contempladas para el MVP son:

- Consultar el comportamiento histórico de materias primas y equipos.
- Obtener predicciones del costo futuro de los equipos dentro del horizonte definido.
- Mostrar el nivel de incertidumbre asociado a cada predicción.
- Responder preguntas sobre los principales hallazgos obtenidos durante el análisis.
- Complementar las respuestas con información externa relevante del mercado cuando esté disponible.
- Exponer el producto mediante una aplicación web desplegada en la nube.

## Versión 2
La siguiente versión del producto buscará ampliar las capacidades analíticas y conversacionales del asistente.

Entre las funcionalidades previstas se encuentran:

- Simulación de escenarios ("¿qué pasaría si...?").
- Comparación de múltiples escenarios de costos.
- Incorporación de nuevos modelos predictivos.
- Monitoreo automático de noticias y tendencias del mercado.
- Alertas sobre cambios relevantes en materias primas.
- Incorporación de memoria conversacional para mantener contexto entre consultas.

## Visión futura
La visión de largo plazo consiste en evolucionar el asistente hacia una plataforma inteligente de apoyo a la planeación de costos operativos.

Entre las capacidades esperadas se consideran:

- Integración con sistemas empresariales (ERP).
- Actualización automática de datos históricos.
- Reentrenamiento periódico de los modelos.
- Incorporación de nuevos tipos de equipos y materias primas.
- Soporte para múltiples proyectos de construcción.
- Generación automática de reportes ejecutivos y análisis comparativos.
- Arquitectura multiusuario con autenticación y gestión de permisos.

---
## Estado actual del desarrollo

**Versión del documento:** MVP v1.0

Estado general del proyecto:

- ✅ Product Guide definido.
- ✅ Notebook 01 convertido en fuente de conocimiento estructurado.
- 🟡 Notebook 02 en proceso de ingeniería de conocimiento.
- ⬜ Notebook 03 pendiente de revisión arquitectónica.
- ⬜ Notebook 04 pendiente de revisión arquitectónica.
- ⬜ Notebook 05 pendiente de construcción.
- ⬜ Construcción de la carpeta `knowledge/`.
- ⬜ Integración con Azure AI Search.
- ⬜ MVP funcional del asistente.


# 6. Registro de Decisiones Arquitectónicas (ADR)

**Estado:** 🟢 Aprobada

Esta sección documenta las decisiones arquitectónicas que definen el diseño del producto. Cada ADR registra el contexto, la decisión adoptada y su justificación. Una ADR aprobada solo podrá modificarse si una decisión posterior reemplaza explícitamente su contenido.

---

## ADR-001 — El proyecto se define como un producto y no como un conjunto de notebooks

**Estado:** 🟢 Aprobada

### Contexto

Inicialmente el desarrollo se encontraba centrado en notebooks de análisis y modelos predictivos. Sin embargo, el entregable final requiere la construcción de un agente de inteligencia artificial orientado al usuario de negocio.

### Decisión
El proyecto se define como un producto de inteligencia artificial denominado **Asistente Inteligente para Planeación de Costos Operativos**.

Los notebooks constituyen la evidencia técnica del análisis, mientras que la definición funcional del producto se documenta en `00_PROJECT_GUIDE.md`.

### Justificación
Esta separación permite evolucionar el producto sin depender de la estructura de los notebooks y establece una clara diferencia entre el análisis científico y el producto final entregado al usuario.

---

## ADR-002 — El MVP será diseñado desde las capacidades del producto

**Estado:** 🟢 Aprobada

### Contexto
Durante la definición del producto surgió la necesidad de evitar que la implementación estuviera guiada por tecnologías específicas o por herramientas individuales.
### Decisión
El diseño del MVP estará dirigido por las capacidades conversacionales del producto y no por la tecnología utilizada para implementarlas.

Toda nueva funcionalidad deberá responder primero a una necesidad del usuario antes de definir su implementación técnica.

### Justificación
Este enfoque mantiene el producto centrado en el valor para el usuario y facilita la evolución de la arquitectura sin modificar el propósito del asistente.

---

## ADR-003 — Separación entre documentación funcional y documentación técnica

**Estado:** 🟢 Aprobada

### Contexto
El proyecto requiere documentar tanto el funcionamiento del producto como la arquitectura tecnológica utilizada para implementarlo.

### Decisión
El archivo `00_PROJECT_GUIDE.md` será la especificación funcional del producto.

La arquitectura cloud, la arquitectura RAG, la base de conocimiento, el despliegue y demás aspectos técnicos se documentarán en archivos independientes dentro de la carpeta `docs/`.

### Justificación
Esta separación permite mantener el documento principal estable, facilita el mantenimiento de la documentación y evita mezclar decisiones funcionales con detalles de implementación.


================
---

**Última actualización:**
Ingeniería de Conocimiento completada para el Notebook 01.
Próxima actividad: Ingeniería de Conocimiento del Notebook 02.

