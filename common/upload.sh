for i in *.py ; do 
  echo "Uploading $i..."
  ampy --port $1 put $i
done
