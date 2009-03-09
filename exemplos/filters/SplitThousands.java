public class SplitThousands {
  
    public static String splitThousands(String str, String sep){
        if(str.length() < 4){
            return str;
        }
        return splitThousands(str.substring(0, str.length() - 3), sep) + sep + str.substring(str.length() - 3, str.length());
    }
    
    public static String splitThousands(String str){
        return splitThousands(str, ",");
    }

    public static void main(String[] args) {
        System.out.println(splitThousands("45168313818651"));
        System.out.println(splitThousands("45168313818651", "."));
    }
}

