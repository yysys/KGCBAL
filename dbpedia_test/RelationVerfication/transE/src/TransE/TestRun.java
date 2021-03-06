package TransE;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

import static TransE.GlobalValue.*;

public class TestRun {

    private static Test test;

    private static int Read_Data(String file_name, Map<String, Integer> data2id, Map<Integer, String> id2data) throws IOException {
        int count = 0;
        File f = new File(file_name);
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(f),"UTF-8"));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] split_data = line.split("\t");
            data2id.put(split_data[0], Integer.valueOf(split_data[1]));
            id2data.put(Integer.valueOf(split_data[1]), split_data[0]);
            count++;
        }
        return count;
    }

    private static void GlobalValueInit() {
        relation2id = new HashMap<>();
        entity2id = new HashMap<>();
        id2relation = new HashMap<>();
        id2entity = new HashMap<>();
        left_entity = new HashMap<>();
        right_entity = new HashMap<>();
        left_num = new HashMap<>();
        right_num = new HashMap<>();
    }

    private static void vec_add_value(Map<Integer, Map<Integer, Integer>> entity_map, int key, int value_k) {
        if (!entity_map.containsKey(key)) {
            entity_map.put(key, new HashMap<>());
        }
        Map<Integer, Integer> entity_value = entity_map.get(key);
        if (!entity_value.containsKey(value_k)) {
            entity_value.put(value_k, 0);
        }
        entity_value.put(value_k, entity_value.get(value_k) + 1);
    }

    private static void prepare(int rate) throws IOException {
        GlobalValueInit();
        entity_num = Read_Data("resource/data/"+ rate + "/entity2id.txt", entity2id, id2entity);
        relation_num = Read_Data("resource/data/" + rate + "/relation2id.txt", relation2id, id2relation);

        File f = new File("resource/data/" + rate + "/test.txt");
        BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(f),"UTF-8"));
        String line;
        while ((line = reader.readLine()) != null) {
            String[] split_data = line.split("\t");
            String head = split_data[0];
            String tail = split_data[1];
            String relation = split_data[2];
            int label = Integer.valueOf(split_data[3]);
            boolean flag = true;
            if (label == 1) {
                flag = true;
            }
            else {
                flag = false;
            }

            if (!entity2id.containsKey(head)) {
                System.out.printf("miss entity: %s\n", head);
            }
            if (!entity2id.containsKey(tail)) {
                System.out.printf("miss entity: %s\n", tail);
            }
            if (!relation2id.containsKey(relation)) {
                relation2id.put(relation, relation_num);
                relation_num++;
            }
            vec_add_value(left_entity, relation2id.get(relation), entity2id.get(head));
            vec_add_value(right_entity, relation2id.get(relation), entity2id.get(tail));

            test.add(entity2id.get(head), relation2id.get(relation), entity2id.get(tail), flag);
        }

        System.out.printf("entity number = %s\n", entity_num);
        System.out.printf("relation number = %s\n", relation_num);
    }

    public static void test_run(int rate) throws IOException {
        test = new Test();
        prepare(rate);
        test.run();
    }

}
