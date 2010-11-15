#include <map>
#include <iostream>
#include <stdio.h>
using namespace std;


/*
 * Adiuvo: to  help, assist
 * This is aimed as a replacement to the sysadmin script which has move from bash to python and now to c++
 * This is hardly going to be a best practises coding as I've not done c++ for several years, and most likely will be living nightmare
 * for most elitist c++ developers, well then don't use it!
 * This is aimed at shortening systems administration tasks, and to aid in diagnostics where required.
 * ~ Copyright 2010 David Busby
 */

// Value-Defintions of the different String values
enum Commands { evNotDefined, 
                          c_List, 
                          evEnd };

// Map to associate the strings with the enum values
static std::map<std::string, Commands> s_mapCommands;

void mapInit(){
	s_mapCommands["list"] = c_List;
}
/**
 * This function will print out usage information
 * @var char *argv[] runtime arguments
 */
void usage(char *prg){
	cout << "Usage: " << prg << " <command>" << endl;
	cout << "i.e. " << prg << " list" << endl;
}

void cList(char *prg){
	cout << "--- Available Command List ---" << endl;
	cout <<  prg << "list - Prints out this information" << endl;
}

/**
 * This function is to test the ability to lock a file at a given path,
 * the need for this arrose when running into NFS lock issues from the application servers to our datastore cluster
 * it will attempt to create a random file at the given path, lock, write data, read data, validate and finaly unlink the file
 **/

void flock(char *path){
	cout << "coming sooooon" << endl;
}

/**
 * Provide memory maping functionality, can be handy for testing
 * allow things such as anano mampping with /dev/zero, and noting diffs between mapped allocation and actual use
 */
void mMap(){
	cout << "coming soon" << endl;
}
/**
 * This function is the main program function
 * @var int argc count of runtime arguments
 * @var char *argv[] runtime arguments
 **/
int main(int argc, char *argv[]){
	mapInit();	
	if (argc < 2){
		cout << "No option was passed!" << endl;
		usage(argv[0]);
	}else if(argc > 2){
		cout << "Too many args!" << endl;
		usage(argv[0]);
	}else{
		switch(s_mapCommands[argv[1]]){
			case c_List:
				cList(argv[0]);
			break;
			default:
				usage(argv[0]);
		}
	}	
	return 0;
}


