function updateGH { 
    for f in /var/lib/docker/volumes/jupyterhub-user-teach*;  do 
        if [ -d $f  -a ! -h $f ];  
        then  
            cd -- "$f/_data/";  
            echo "Doing something in folder `pwd`/$f";
	    ls -- "$f/_data/";
	    mkdir -- "$f/_data/oldFolders"
	    mv $f/_data/popModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-popModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingPop.git $f/_data/popModelling
	    chmod 777 -R $f/_data/
        fi;  
    done;  
};
updateGH
