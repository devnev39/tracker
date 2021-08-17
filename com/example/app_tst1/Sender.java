package com.example.app_tst1;

import java.io.Serializable;
import java.util.HashMap;

public class Sender implements Serializable {
    private static final long serialVersionUID = 6529685098267757690L;
    public static enum Properties {
        Acceleration,
        Gravity,
        Gyro,
        Rotation,
        MagField,
        Orientation,
        Light
    }

    public HashMap<Properties,Object> values;

    public HashMap<Properties,Object> getValues(){
        return values;
    }
}
