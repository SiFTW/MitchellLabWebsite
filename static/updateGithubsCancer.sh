#!/bin/bash
function updateGH { 
    for f in /var/lib/docker/volumes/jupyterhub-user-teach*;  do 
        if [ -d $f  -a ! -h $f ];  
        then  
            cd -- "$f/_data/";  
            echo "Doing something in folder `pwd`/$f";
	    ls -- "$f/_data/";
	    mkdir -- "$f/_data/oldFolders"
	    mv $f/_data/cancerModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-cancerModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingCancer.git $f/_data/cancerModelling
	    chmod 777 -R $f/_data/
        fi;  
    done;  
};
updateGH
