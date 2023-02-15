DIR=${PWD}/work

smooths=("backoff" "interpolate")
discounts=("ukndiscount" "kndiscount" "wbdiscount")

for smth in ${smooths[@]}; do
  for dis in ${discounts[@]}; do
	if [ -d "$DIR" ];
	then
        	source clean.sh
	fi
	source launcher.sh -n 4 -i 3 -s ${smth} -d ${dis} 
  done
done

