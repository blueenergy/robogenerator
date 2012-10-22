//import test.TestApi;
package test;  

public class TestJava 
 
{   
	Time times [] = {new Time(19,42,42),new Time(1,23,54),new Time(5,3,2)} ;  
    public TestJava() 
	{
	int a[] = {0,1,2} ;     
     
    }
	public Time[] getTimeList()
	{
	    return times;
	}

    public static void main(String[] args)  
    {  

        //test.TestApi instance = new test.TestApi();
        //String a = instance.getData("aaa");
        //System.out.println(a);
        String str = "how are you doing this?";
        //instance.printData(str);
  
    }

} 
class Time     
{     
     int hour,min,sec ;     
     Time(int hour ,int min ,int sec) {     
         this.hour = hour ;     
         this.min = min ;     
         this.sec = sec ;     
     }     
}     