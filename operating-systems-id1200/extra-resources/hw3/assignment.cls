\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{assignment}[a latex class for editing your assignment]

\LoadClass[11pt,letterpaper]{article}
\RequirePackage{amsmath}
\RequirePackage[left=2cm,right=2cm,top=1.5cm,bottom=2cm]{geometry}
\RequirePackage[dvipsnames]{xcolor}
\RequirePackage{listings}
\RequirePackage[most]{tcolorbox}
\newtcolorbox[]{myBox}[1][]{
      attach boxed title to top left={xshift=0.5cm, yshift=-2mm},
      title=#1,
      breakable,
      left = 0.5cm,
    enhanced,
    arc=2pt,
    outer arc=2pt,
    boxrule=1pt,
    left=3pt,
    right=3pt,
    top=3pt,
    bottom=3pt,
    fontupper=\small,
}

\usepackage[dvipsnames]{xcolor}
\definecolor{Mycolor1}{HTML}{059C9C}


\setlength{\textwidth}{6.5in}
\setlength{\textheight}{9.in}
\setlength{\oddsidemargin}{0in}
\setlength{\headheight}{0in}


% create a box to highlight word
\newtcbox{\hword}[1][orange]{on line, arc = 0.3mm,auto outer arc,colback = #1!12!, colframe = #1!60!,colupper = black, boxsep =0mm, left =0.3mm, right = 0.3mm, top =0.4mm, bottom = 0.4mm,boxrule =0.2mm, bottomrule =0.2mm, toprule = 0.2mm}

% highlight equations in align envoirnment or with $$
\newcommand{\hmath}[1]{\hword{\text{\( #1 \)}}}


% small note in an align
\newcommand{\step}[1]{\text{ \tiny{#1}}}


\lstset{
    framerule=1pt,
    frame=tb,
    emphstyle={\small\ttfamily\bfseries\color{Orange}},
    numbers=left,
    numberstyle= \tiny\color{black},
    basicstyle = \small\ttfamily,
    keywordstyle    = \bfseries\color{Mycolor1},
    identifierstyle = \bfseries\color{Red!100},
    stringstyle     = \bfseries\color{green!10!orange},
    commentstyle    = \bfseries\color{Gray!100},
    % functionstyle    = \bfseries\color{Violet},
    breaklines      =   true,
    columns         =   fixed,
    basewidth       =   .5em,
    backgroundcolor=\color{Gray!15},
    tabsize=2,
    showspaces=false,
    showstringspaces=false,
}

\newcommand{\assignmentTitle}[7]{
    \begin{center}
        \vspace{-16mm}
    \includegraphics[height=2cm]{#1}
    \end{center}
    
    \begin{center}
        \vspace{0cm}
    
    \text{\Large #2} \\ % where the course name goes
    \text{\Large #3} \\ % where the assignment name goes
    \text{#4} \\ % course code
    \text{\today} \\ %the date 
    \text{#5}\\ % names
    \text{#6} %emails
    \end{center}
   \noindent\rule{\linewidth}{.6pt}
%   \tableofcontents
}
