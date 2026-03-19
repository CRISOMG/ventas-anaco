# **Guía de Metodologías Ágiles y Lean para la Ejecución**

**Proyecto:** "Cuota Cero" \- Ventas Anaco

**Objetivo del Documento:** Proveer marcos de trabajo (frameworks) para el discernimiento diario en la administración y ejecución operativa del proyecto.

## **Introducción al Discernimiento Diario**

Para gestionar el proyecto "Cuota Cero" sin caer en la microgestión ni en el caos, el equipo gestor debe utilizar metodologías probadas de la industria del software y la manufactura, adaptadas al comercio minorista. Este documento define las herramientas metodológicas para equilibrar la agilidad de ventas con el rigor del control de créditos.

## **1\. El Manifiesto Agile (Agilidad en Ventas y Desarrollo)**

Agile no es hacer las cosas rápido y mal; es la capacidad de adaptarse rápidamente al cambio. Para el proyecto "Cuota Cero", adoptamos los siguientes valores del manifiesto:

* **Individuos e interacciones sobre procesos y herramientas:** Si el Excel actual (herramienta) frena al equipo de ventas (individuos), se cambia la herramienta.  
* **Soluciones operativas sobre documentación excesiva:** Es mejor tener un Google Form funcional hoy que capture clientes, a tener un manual de 100 páginas de un sistema que no existe.  
* **Colaboración con el cliente sobre negociación contractual:** Escuchar qué productos de ticket bajo el cliente *realmente* quiere llevarse a "cuota cero" en lugar de forzar el inventario que nosotros queremos empujar.  
* **Respuesta ante el cambio sobre seguir un plan:** Si la línea de suministro de China cambia los costos, el sistema de cuotas debe poder recalcularse el mismo día.

## **2\. Principios de Scrum (Ritmo de Ejecución)**

Scrum se utilizará para dividir la gran meta de la transición tecnológica y el lanzamiento comercial en ciclos de trabajo manejables (Sprints).

* **El Sprint (Ciclo de trabajo):** Periodos cortos (ej. 1 o 2 semanas) con un objetivo claro. *Ejemplo de Sprint: "Migrar el registro de los 50 productos más vendidos del Excel a BigQuery".*  
* **Roles en Ventas Anaco:**  
  * **Product Owner (Dueños/Stakeholders):** Definen el "Qué" (la visión del negocio y qué funciones del sistema aportan más valor).  
  * **Scrum Master (El Rol Gestor/TPM):** Facilita el proceso, elimina los bloqueos (ej. "el internet falló", "la persona de inventario no entiende el sistema") y protege al equipo.  
  * **Equipo de Ejecución:** Quienes operan la data y atienden al cliente.  
* **Ceremonias Clave:**  
  * **Daily Stand-up (Reunión Diaria de 15 min):** ¿Qué hicimos ayer? ¿Qué haremos hoy? ¿Qué nos bloquea? (Fundamental para el discernimiento diario).

## **3\. Filosofía Lean (Eficiencia y Eliminación de Desperdicio)**

Lean se enfoca en maximizar el valor para el cliente mientras se minimizan los desperdicios (*Muda*).

* **Lean Canvas (Para la estrategia comercial):** Se utilizará para iterar el modelo de negocio rápidamente. ¿Quién es el segmento exacto para la "Cuota Cero"? ¿Cuál es nuestra ventaja injusta (nuestra cadena de suministro de China)?  
* **Lean Operations (Operaciones Esbeltas):** En el contexto de "Cuota Cero", significa eliminar cualquier paso que no agregue valor.  
  * *Ejemplo de desperdicio a eliminar:* La doble digitación. Si un vendedor anota el crédito en un cuaderno y luego la administradora lo pasa a Excel, hay desperdicio de tiempo y riesgo de error. Lean exige automatizar ese flujo (ej. Entrada directa a Google Forms desde el teléfono del vendedor).

## **4\. Six Sigma y Lean Six Sigma (El Foco en el "Control")**

Mientras que Agile busca velocidad (Éxito) y Lean busca eficiencia, Six Sigma asegura la **Calidad (Control)**.

* **¿Qué es Six Sigma?** Es una metodología de mejora de procesos basada en datos que busca eliminar casi por completo los defectos (estadísticamente, busca no tener más de 3.4 defectos por millón de oportunidades).  
* **Lean Six Sigma:** Combina la velocidad y eliminación de desperdicio de Lean, con el rigor matemático y la reducción de errores de Six Sigma.  
* **Aplicación en la "Cuota Cero":** Un "defecto" en un ecosistema de créditos es dinero perdido (un cobro mal calculado, un cliente no registrado, un inventario fantasma).  
* **Metodología DMAIC para el Control de Datos:** El equipo gestor usará este ciclo para arreglar el problema del Excel actual:  
  1. **D**efinir: El problema es que Excel permite la sobreescritura accidental de cuotas pagadas.  
  2. **M**edir: Cuántos errores de facturación sucedieron el mes pasado por culpa de Excel.  
  3. **A**nalizar: La causa raíz es que no hay permisos de usuario; todos editan el mismo archivo.  
  4. **I**mplementar (Improve): Migrar la captura de datos a un sistema estandarizado (AppSheet / Google Cloud) donde los vendedores solo pueden "agregar" datos, no borrarlos.  
  5. **C**ontrolar: Crear un Dashboard en Looker Studio que alerte automáticamente si hay discrepancias en la caja.

## **5\. El Discernimiento Diario (La Fusión Práctica)**

El TPM / Asistente Informático tomará decisiones diarias cruzando estas metodologías con la brújula del proyecto:

1. **Si el problema requiere Innovación y Salida al Mercado (Éxito):** Usa **Agile & Scrum**. Lanza un piloto rápido, prueba si el cliente acepta la cuota cero en un producto nuevo, itera la oferta.  
2. **Si el problema es de Cuellos de Botella Operativos:** Usa **Lean**. Observa el proceso, identifica el desperdicio (tiempos muertos, burocracia) y simplifica el flujo de trabajo de los empleados.  
3. **Si el problema es de Pérdida Financiera o Fallos de Data (Control):** Usa **Six Sigma**. Detén la operación, audita la base de datos de créditos, encuentra la raíz matemática del error y diseña un sistema a prueba de tontos (Poka-Yoke) para que no vuelva a ocurrir.