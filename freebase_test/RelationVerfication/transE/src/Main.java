import TransE.TestRun;
import TransE.TrainRun;

import java.io.*;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) throws IOException {
        System.out.println("Train or test? y/n");
        Scanner sc = new Scanner(System.in);
        boolean train_flag;
        train_flag = sc.next().equals("y");
        System.out.println("which rate:");
        int rate = sc.nextInt();
        if (rate != 55 && rate != 60 && rate != 65 && rate != 70 && rate != 75 && rate != 80 && rate != 85) {
            System.out.println("error!");
            return;
        }
        if (train_flag) {
            System.out.println("Begin train");
            TrainRun.train_run(rate);
        } else {
            System.out.println("Begin test");
            TestRun.test_run(rate);
        }
    }
}