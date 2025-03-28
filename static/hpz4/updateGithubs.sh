#!/bin/bash
function updateGH { 
    for f in /var/lib/docker/volumes/jupyterhub-user-student*;  do 
        if [ -d $f  -a ! -h $f ];  
        then
	    if [ ! -d "$f/_data/" ]; then
		echo "$_data does not exist."
		mkdir -- "$f/_data/"
	    fi
            cd -- "$f/_data/";  
            echo "Doing something in folder `pwd`/$f";	    
	    ls -- "$f/_data/";
	    mkdir -- "$f/_data/oldFolders"
	    mv $f/_data/MDModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-MDModelling
	    mv $f/_data/cancerModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-cancerModelling
	    mv $f/_data/popModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-popModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingPop.git $f/_data/popModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingCancer.git $f/_data/cancerModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingMD.git $f/_data/MDModelling
	    chmod 777 -R $f/_data/
        fi;  
    done;  
};
updateGH
