% dfcards.cls -- flashcards in the shape of konradcinkusz/csharp-flashcards:
% a question slide, then an answer frame, a category badge top right, a 1-3 difficulty
% rating. It is a LIGHT sibling of that repository's mybeamer.cls on purpose: this book
% needs no minted (no code), no fontawesome5 and no xelatex, so the deck builds with
% plain pdflatex on any TeX Live. The card mechanic and the macro names are the same.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{dfcards}[2026/11/01 German flashcards, light]
\LoadClass[aspectratio=169,14pt]{beamer}
\RequirePackage[T1]{fontenc}
\RequirePackage[utf8]{inputenc}
\RequirePackage{lmodern}
\RequirePackage[ngerman,main=polish]{babel}
\RequirePackage{tikz}
\RequirePackage{xcolor}

\newcommand{\RepoSlug}{konradcinkusz/german-from-zero-to-hero}
\newcommand{\RepoURL}{https://github.com/\RepoSlug}
\definecolor{lvA1}{RGB}{39,174,96}
\definecolor{lvA2}{RGB}{41,128,185}
\definecolor{lvB1}{RGB}{230,126,34}
\definecolor{lvB2}{RGB}{142,68,173}

\setbeamertemplate{navigation symbols}{}
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamercolor{frametitle}{fg=black,bg=white}
\setbeamertemplate{footline}{%
  \leavevmode\hbox{\begin{beamercolorbox}[wd=\paperwidth,ht=2.5ex,dp=1ex,leftskip=1em,rightskip=1em]{author in head/foot}
  \scriptsize\href{\RepoURL}{\RepoSlug}\hfill\insertframenumber\end{beamercolorbox}}}

\newcounter{qcounter}
\newcommand{\Difficulty}[1]{%
  \ifcase#1\or $\bullet\circ\circ$\or $\bullet\bullet\circ$\or $\bullet\bullet\bullet$\fi}
% \CategoryBadge{level}{category}
\newcommand{\CategoryBadge}[2]{%
  \colorbox{lv#1!20}{\strut\textcolor{lv#1!70!black}{\textbf{#1}\,\footnotesize #2}}}
\newcommand{\BadgeOverlay}[3]{%
  \begin{tikzpicture}[remember picture,overlay]
    \node[anchor=north east,xshift=-0.4cm,yshift=-0.4cm] at (current page.north east)
      {\CategoryBadge{#1}{#2}\,\Difficulty{#3}};
  \end{tikzpicture}}

% \Card{level}{category}{difficulty 1-3}{question}{answer}
\newcommand{\Card}[5]{%
  \stepcounter{qcounter}%
  \begin{frame}
    \BadgeOverlay{#1}{#2}{#3}%
    \centering\vfill{\Large \theqcounter.\ #4\par}\vfill
  \end{frame}%
  \begin{frame}
    \BadgeOverlay{#1}{#2}{#3}%
    \frametitle{Odpowiedź \theqcounter}%
    \centering\vfill{\large #5\par}\vfill
  \end{frame}}
