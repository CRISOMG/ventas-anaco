# Documento de Diseño Técnico: Estilos y Composición

Este documento define las reglas de diseño, paletas de colores, tipografía y componentes estructurales basados en `informe.html` e `index.html` para la creación de nuevos documentos HTML consistentes.

## 1. Fundamentos Visuales

### Framework y Herramientas
- **CSS:** Tailwind CSS (vía CDN).
- **Fuentes:** Inter (`sans-serif`).
- **Iconografía:** Phosphor Icons (vía CDN).
- **Interactividad:** Chart.js (para reportes de datos).

### Paleta de Colores Principal (Brand)
| Color | Hex | Uso Sugerido |
| :--- | :--- | :--- |
| **Brand 900** | `#1e3a8a` | Encabezados principales, Sidebar. |
| **Brand 700** | `#1d4ed8` | Enlaces, estados de hover. |
| **Brand 500** | `#3b82f6` | Acentos primarios, iconos. |
| **Brand 100** | `#dbeafe` | Fondos de badges, secciones ligeras. |
| **Slate 900** | `#0f172a` | Texto de cuerpo principal. |
| **Slate 50** | `#f8fafc` | Fondo general de página. |

## 2. Composición y Layout

### Estructura de Reporte (Tipo Informe)
- **Navegación:** Sidebar lateral izquierdo (fijo en desktop, scroll horizontal en móvil).
- **Contenido:** Área principal (`main`) con `max-w-5xl` y espaciado generoso (`space-y-16`).
- **Secciones:** Uso de `scroll-mt-8` para alineación de enlaces internos.

### Estructura de Propuesta (Tipo Landing)
- **Navegación:** Barra superior sticky con efecto de elevación (shadow).
- **Hero Section:** Gradiente de fondo (`from-blue-700 via-blue-600 to-blue-800`) y texto centrado.
- **Secciones:** Fondos alternados (blanco y `blue-50`) con bordes redondeados grandes (`rounded-3xl`).

## 3. Componentes Reutilizables

### Glass Card
```html
<div class="bg-white/95 backdrop-blur-md border border-slate-200/80 rounded-2xl p-6 shadow-sm">
    <!-- Contenido -->
</div>
```

### Icon Box
```html
<div class="w-14 h-14 rounded-2xl flex items-center justify-center text-2xl font-bold bg-brand-100 text-brand-600">
    <i class="ph-fill ph-rocket"></i>
</div>
```

### Secciones con Indicador de Estado (Phases/Cards)
- **Borde Superior:** `border-t-4` con colores semánticos (Rojo: Riesgo, Azul: Info, Verde: Éxito).
- **Borde Lateral:** `border-l-8` para destacar características clave.

## 4. Tipografía y Jerarquía
- **H1/Hero:** `text-4xl md:text-5xl font-extrabold tracking-tight`.
- **H2/Sección:** `text-2xl font-bold text-slate-800`.
- **Cuerpo:** `text-slate-600 leading-relaxed`.
- **Badges:** `rounded-full px-3 py-1 font-semibold text-xs uppercase`.

## 5. Mejores Prácticas de Implementación
1. **Responsive First:** Asegurar que las grillas (`grid-cols-1 md:grid-cols-2/3`) funcionen en móviles.
2. **Micro-interacciones:** Agregar transiciones suaves (`transition-all duration-300`) en elementos interactivos y hovers.
3. **Semántica:** Utilizar etiquetas `header`, `main`, `section`, `footer` y `article` correctamente.
4. **Metadatos:** Incluir siempre etiquetas `og:title` y `viewport` para una visualización profesional en redes y dispositivos móviles.
