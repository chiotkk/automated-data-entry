import crop
import preprocess
import MLP
import excel
from keras.models import load_model


def main():
    print('Train new weights or load existing weights?')
    print('1: Train new weights')
    print('2: Load existing weights')
    x = input()
    if x == '1':
        print('Training neural network...')
        model = MLP.train()
        print('Neural network training complete!')
        model.save('MLP.h5')
    else:
        print('Loading neural network...')
        model = load_model('MLP.h5')
        print('Neural network loading complete!')


    file_name = input('Enter file name: ')
    print('Processing scanned invoice...')
    x, y = crop.finder(file_name)
    crop.crop_invoice(x, y, file_name)
    preprocess.prep_input()

    print('Updating excel file...')
    serial = MLP.get_serial(model)
    date = MLP.get_date(model)
    excel.add_date(date)
    values, unit_check = MLP.get_data(model)
    excel.check_values(values, unit_check)
    excel.add_values(values)
    print('Excel file updated!')


if __name__ == '__main__':
    main()
