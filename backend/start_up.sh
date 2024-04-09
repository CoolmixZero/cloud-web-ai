cd app

uvicorn main:app --host 127.0.0.1 --port 5000

# case "$OSTYPE" in
#   linux*)
#     echo "LINUX"
#     # Run gunicorn on Linux
#     cd app
#     gunicorn api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 127.0.0.1:5000
#     ;;
#   msys*)
#     echo "WINDOWS (MSYS)"
#     # Run waitress-serve on Windows with MSYS
#     cd app
#     waitress-serve --listen=127.0.0.1:5000 main:app
#     # python -m uvicorn main:app --host 127.0.0.1 --port 5000
#     ;;
#   cygwin*)
#     echo "WINDOWS (CYGWIN)"
#     # Run waitress-serve on Windows with Cygwin
#     cd app
    
#     waitress-serve --listen=127.0.0.1:5000 api:app
#     ;;
#   *)
#     echo "Unsupported operating system: $OSTYPE"
#     exit 1
#     ;;
# esac
