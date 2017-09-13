for d in */
do
  echo $d
  for f in $d*.txt
  do
    echo $f
    ### DO i Need to replace !'s with .'s before sending to Tree Tagger?
    cat $f | tree-tagger-latin > $f.pos
    python ../preProcess.py $f.pos | python ../removeDoubles.py > $f
    #rm $f.pos
  done
done

echo
echo Done POS tagging $d
echo
