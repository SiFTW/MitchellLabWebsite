function updateGH { 
    for f in /var/lib/docker/volumes/jupyterhub-user-teach*;  do 
        if [ -d $f  -a ! -h $f ];  
        then  
            cd -- "$f/_data/";  
            echo "Doing something in folder `pwd`/$f";
	    ls -- "$f/_data/";
	    mkdir -- "$f/_data/oldFolders"
	    mv $f/_data/MDModelling $f/_data/oldFolders/$(date +"%H%M-%d-%m-%Y")-MDModelling
	    git clone https://github.com/SiFTW/MitchellLabTeachingMD.git $f/_data/MDModelling
	    chmod 777 -R $f/_data/
        fi;  
    done;  
};
updateGH
