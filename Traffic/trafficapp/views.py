from django.shortcuts import render

def Traffic(request):
    if(request.method == "POST"):
        data = request.POST
        path = data.get("imageUpload")
        if ('buttonsubmit'in request.POST):
            import numpy as np 
            import pandas as pd 
            import matplotlib.pyplot as plt
            import cv2
            import tensorflow as tf
            from PIL import Image
            import os
            os.chdir('C:\\Users\\DELL\\OneDrive\\Desktop\\DVMP\\Traffic_Sign_Detection')
            from sklearn.model_selection import train_test_split
            from keras.utils import to_categorical
            from keras.models import Sequential, load_model
            from keras.layers import Conv2D, MaxPool2D, Dense, Flatten, Dropout
            data = []
            labels = []
            classes = 43
            cur_path = os.getcwd()
            for i in range(classes):
                path = os.path.join(cur_path,'Train',str(i))
                images = os.listdir(path)
                for a in images:
                    try:
                        image = Image.open(path + '\\'+ a)
                        image = image.resize((30,30))
                        image = np.array(image)
                        data.append(image)
                        labels.append(i)
                    except Exception as e:
                        print(e)
            data = np.array(data)
            labels = np.array(labels)
            np.save('./training/data',data)
            np.save('./training/target',labels)
            data=np.load('./training/data.npy')
            labels=np.load('./training/target.npy')
            X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=0)
            y_train = to_categorical(y_train, 43)
            y_test = to_categorical(y_test, 43)
            model = Sequential()
            model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu', input_shape=X_train.shape[1:]))
            model.add(Conv2D(filters=32, kernel_size=(5,5), activation='relu'))
            model.add(MaxPool2D(pool_size=(2, 2)))
            model.add(Dropout(rate=0.25))
            model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
            model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu'))
            model.add(MaxPool2D(pool_size=(2, 2)))
            model.add(Dropout(rate=0.25))
            model.add(Flatten())
            model.add(Dense(256, activation='relu'))
            model.add(Dropout(rate=0.5))
            model.add(Dense(43, activation='softmax'))
            model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
            epochs = 20
            history = model.fit(X_train, y_train, batch_size=32, epochs=epochs, validation_data=(X_test, y_test))
            def testing(testcsv):
                y_test = pd.read_csv(testcsv)
                label = y_test["ClassId"].values
                imgs = y_test["Path"].values
                data=[]
                for img in imgs:
                    image = Image.open(img)
                    image = image.resize((30,30))
                    data.append(np.array(image))
                X_test=np.array(data)
                return X_test,label
            X_test, label = testing('Test.csv')
            Y_pred = model.predict(X_test)
            y_pred = np.argmax(Y_pred, axis=-1)
            from sklearn.metrics import accuracy_score
            acc=accuracy_score(label, y_pred)
            model.save("./training/TSR.h5")
            import os
            os.chdir(r'C:\\Users\\DELL\\OneDrive\\Desktop\\DVMP\\Traffic_Sign_Detection')
            from keras.models import load_model
            model = load_model('./training/TSR.h5')
            classes = { 0:'Speed limit (20km/h)',
            1:'Speed limit (30km/h)', 
            2:'Speed limit (50km/h)', 
            3:'Speed limit (60km/h)', 
            4:'Speed limit (70km/h)', 
            5:'Speed limit (80km/h)', 
            6:'End of speed limit (80km/h)', 
            7:'Speed limit (100km/h)', 
            8:'Speed limit (120km/h)', 
            9:'No passing', 
            10:'No passing veh over 3.5 tons', 
            11:'Right-of-way at intersection', 
            12:'Priority road', 
            13:'Yield', 
            14:'Stop', 
            15:'No vehicles', 
            16:'Veh > 3.5 tons prohibited', 
            17:'No entry', 
            18:'General caution', 
            19:'Dangerous curve left', 
            20:'Dangerous curve right', 
            21:'Double curve', 
            22:'Bumpy road', 
            23:'Slippery road', 
            24:'Road narrows on the right', 
            25:'Road work', 
            26:'Traffic signals', 
            27:'Pedestrians', 
            28:'Children crossing', 
            29:'Bicycles crossing', 
            30:'Beware of ice/snow',
            31:'Wild animals crossing', 
            32:'End speed + passing limits', 
            33:'Turn right ahead', 
            34:'Turn left ahead', 
            35:'Ahead only', 
            36:'Go straight or right', 
            37:'Go straight or left', 
            38:'Keep right', 
            39:'Keep left', 
            40:'Roundabout mandatory', 
            41:'End of no passing', 
            42:'End no passing veh > 3.5 tons' }
            from PIL import Image
            import numpy as np
            import matplotlib.pyplot as plt
            def test_on_img(img):
                data=[]
                image = Image.open(img)
                image = image.resize((30,30))
                data.append(np.array(image))
                X_test=np.array(data)
                Y_pred = model.predict(X_test)
                y_pred = np.argmax(Y_pred, axis=-1)
                return image,y_pred
            plot,prediction = test_on_img(path)
            s = [str(i) for i in prediction] 
            a = int("".join(s)) 
            result = "Predicted traffic sign is: "+ classes[a]
            return render(request,'base.html',context={'result':result})
    return render(request,'base.html')