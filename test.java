public class test {
    void run(String[] args) {
        Integer num;

        if (args.length == 0)
            num = 16;
        else
            num = Integer.valueOf(args[0]);

        System.out.printf("answer = %f%n", Math.sqrt(num));

    }

    public static void main(String[] args) {
        test app = new test();
        app.run(args);
    }
}
