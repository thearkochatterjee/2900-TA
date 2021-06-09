#include <string>
#include <windows.h>
#include <iostream>
using namespace std;

string getexepath()
{
	char result[MAX_PATH];
	return std::string(result, GetModuleFileName(NULL, result, MAX_PATH));
}

int main() {
	cout << getexepath();
	return 0;
}