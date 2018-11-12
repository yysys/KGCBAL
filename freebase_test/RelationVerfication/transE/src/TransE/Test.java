package TransE;
import java.io.*;
import java.util.*;

import static TransE.GlobalValue.*;
import static TransE.Gradient.calc_sum;

public class Test {
    // region private members
    private ArrayList<Integer> fb_h;
    private ArrayList<Integer> fb_t;
    private ArrayList<Integer> fb_r;
    private ArrayList<Boolean> label;
    private Map<Pair<Integer, Integer>, Set<Integer>> head_relation2tail; // to save the (h, r, t)
    // endregion

    Test() {
        fb_h = new ArrayList<>();
        fb_t = new ArrayList<>();
        fb_r = new ArrayList<>();
        label = new ArrayList<>();
        head_relation2tail = new HashMap<>();
    }

    public void add(int head, int relation, int tail, boolean flag) {
        fb_h.add(head);
        fb_r.add(relation);
        fb_t.add(tail);
        label.add(flag);
    }

    private void Read_Vec_File(String file_name, double[][] vec) throws IOException {
        File f = new File(file_name);
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(f),"UTF-8"));
        String line;
        for (int i = 0; (line = reader.readLine()) != null; i++) {
            String[] line_split = line.split("\t");
            for (int j = 0; j < vector_len; j++) {
                vec[i][j] = Double.valueOf(line_split[j]);
            }
        }
    }

    private void relation_add(Map<Integer, Integer> relation_num, int relation) {
        if (!relation_num.containsKey(relation)) {
            relation_num.put(relation, 0);
        }
        int count = relation_num.get(relation);
        relation_num.put(relation, count + 1);
    }

    private void map_add_value(Map<Integer, Integer> tmp_map, int id, int value) {
        if (!tmp_map.containsKey(id)) {
            tmp_map.put(id, 0);
        }
        int tmp_value = tmp_map.get(id);
        tmp_map.put(id, tmp_value + value);
    }

    private boolean hrt_isvalid(int head, int relation, int tail) {
        /**
         * 如果实体之间已经存在正确关系，则不需要计算距离
         * 如果头实体与尾实体一致，也排除该关系的距离计算
         */
        if (head == tail) {
            return true;
        }
        Pair<Integer, Integer> key = new Pair<>(head, relation);
        Set<Integer> values = head_relation2tail.get(key);
        if (values == null || !values.contains(tail)) {
            return false;
        } else {
            return true;
        }
    }

    public double distance(double[] h_vec, double[] r_vec, double[] t_vec) {

        double dis = 0;
        for (int i = 0; i < vector_len; i++) {
            dis += (h_vec[i] + r_vec[i] - t_vec[i]) * (h_vec[i] + r_vec[i] - t_vec[i]);
        }

        return Math.sqrt(dis);
    }

    public void run() throws IOException {
        relation_vec = new double[relation_num][vector_len];
        entity_vec = new double[entity_num][vector_len];

        Read_Vec_File("resource/result/relation2vec.bern", relation_vec);
        Read_Vec_File("resource/result/entity2vec.bern", entity_vec);

        double TP = 0, FP = 0, TN = 0, FN = 0;

        for (int i = 0; i < fb_h.size(); i++) {

            double[] h_vec = entity_vec[fb_h.get(i)];
            double[] r_vec = relation_vec[fb_r.get(i)];
            double[] t_vec = entity_vec[fb_t.get(i)];
            boolean flag = label.get(i);

            double dis = distance(h_vec, r_vec, t_vec);

            boolean pred;

            if (dis < 1.2) {
                pred = true;
            }
            else {
                pred = false;
            }

            if (pred == true) {
                if (flag == true) {
                    TP = TP + 1;
                } else {
                    FP = FP + 1;
                }
            }
            else {
                if (flag == true) {
                    FN = FN + 1;
                } else {
                    TN = TN + 1;
                }
            }
        }

        double precision = TP / (TP + FP);
        double recall = TP / (TP + FN);
        double accuracy = (TP + TN) / (TP + FP + TN + FN);
        double F1 = (2.0 * TP) / (2.0 * TP + FP + FN);

        System.out.println("TP: " + TP + " FP: "+ FP + " TN: " + TN + " FN: " + FN);
        System.out.println("precision: " + precision);
        System.out.println("recall: " + recall);
        System.out.println("accuracy: " + accuracy);
        System.out.println("F1: " + F1);
    }
}
