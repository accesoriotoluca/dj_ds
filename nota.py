"""
* EJEMPLO
! EJEMPLO
? EJEMPLO
TODO: EJEMPLO

git config --global user.name "tu_nombre_de_usuario"
git config --global user.email "tu_correo_electrónico"

? GOOGLEAR ARCHIVOS:
asgi/wsgi: por que 'asgy'?
'import os'
'from django.core.asgi import get_asgi_application'
'os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reports_proj.settings')'
'application = get_asgi_application()'

? tutorial de signals?

? desintalar framework:
pip uninstall Django
pip install Django==3.1.7

? comandos en cmd:
pwd=cd y ls=dir, mv=ren, cd ..

? instalar desde requirements.txt:
cd desktop
virtualenv test
cd test
.\Scripts\activate
pip install -r requirements.txt

!-----------------------------------------------------------------------------

[BASE_DIR / 'templates'],

STATIC_URL = 'static/'

STATICFILES_DIRS=[
    BASE_DIR / 'static',
    BASE_DIR / 'sales' / 'static'
]

MEDIA_URL ='/media/'

MEDIA_ROOT=BASE_DIR / 'media'

!-----------------------------------------------------------------------------

usage: git [-v | --version] [-h | --help] [-C <path>] [-c <name>=<value>]
           [--exec-path[=<path>]] [--html-path] [--man-path] [--info-path]
           [-p | --paginate | -P | --no-pager] [--no-replace-objects] [--bare]
           [--git-dir=<path>] [--work-tree=<path>] [--namespace=<name>]
           [--config-env=<name>=<envvar>] <command> [<args>]

These are common Git commands used in various situations:

start a working area (see also: git help tutorial)
   clone     Clone a repository into a new directory
   init      Create an empty Git repository or reinitialize an existing one

work on the current change (see also: git help everyday)
   add       Add file contents to the index
   mv        Move or rename a file, a directory, or a symlink
   restore   Restore working tree files
   rm        Remove files from the working tree and from the index

examine the history and state (see also: git help revisions)
   bisect    Use binary search to find the commit that introduced a bug
   diff      Show changes between commits, commit and working tree, etc
   grep      Print lines matching a pattern
   log       Show commit logs
   show      Show various types of objects
   status    Show the working tree status

grow, mark and tweak your common history
   branch    List, create, or delete branches
   commit    Record changes to the repository
   merge     Join two or more development histories together
   rebase    Reapply commits on top of another base tip
   reset     Reset current HEAD to the specified state
   switch    Switch branches
   tag       Create, list, delete or verify a tag object signed with GPG

collaborate (see also: git help workflows)
   fetch     Download objects and refs from another repository
   pull      Fetch from and integrate with another repository or a local branch
   push      Update remote refs along with associated objects

"""