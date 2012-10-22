package graph_algorithm;  

public class Transition   
{     
     String name;
     int start,end ;     
     Transition(String name ,int start ,int end) {     
         this.name = name ;     
         this.start = start ;     
         this.end = end ;     
     } 
     public void printElement(){
    	 System.out.println(this.name);
    	 System.out.println(this.start);
    	 System.out.println(this.end);
    	 
     }
    	 
     public String getName() {
    	 return this.name;
     }
     public int getStart() {
    	 return this.start;
     }
     public int getEnd() {
    	 return this.end;
     }
     
}   