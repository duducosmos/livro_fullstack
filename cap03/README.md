# Instala��o

O curse j� vem pr� instalado nos sistemas unix e linux, por�m n�o � um m�dulo nativo no window.
Para rodar o jogo da velha no Windows � preciso instalar o modulo. 
A instala��o do m�dulo vai depender da vers�o do Python instalado na sua m�quina, 32bits ou amd64.

Os arquivos para instalar o curse no Windows est�o dispon�veis em: http://www.lfd.uci.edu/~gohlke/pythonlibs/#curses

Para instalar a vers�o para o Python 32 bits use o comando

```
pip install curses-2.2-cp36-cp36m-win32.whl
```

Para vers�es 64 bit

```
pip install curses-2.2cp36-cp36m-win_amd64.whl
```

Alternativamente pode-se tentar o comando:

```
python -m pip install curses-2.2cp36-cp36m-win_amd64.whl
```