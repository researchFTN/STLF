from re import VERBOSE

EPOCH_NUMBER = 15
BATCH_SIZE_NUMBER = 1
COST_FUNCTION = 'mean_squared_error'
OPTIMIZER = 'adam'
KERNEL_INITIALIZER = 'normal'
ACTIVATION_FUNCTION = 'sigmoid'
NUMBER_OF_HIDDEN_LAYERS = 2
NUMBER_OF_NEURONS_IN_FIRST_HIDDEN_LAYER = 10
NUMBER_OF_NEURONS_IN_OTHER_HIDDEN_LAYERS = 6
VERBOSE = 2

class AnnBase:

    def __init__(self):
        self.epoch_number = EPOCH_NUMBER
        self.batch_size_number = BATCH_SIZE_NUMBER
        self.cost_function = COST_FUNCTION
        self.optimizer = OPTIMIZER
        self.kernel_initializer = KERNEL_INITIALIZER
        self.activation_function = ACTIVATION_FUNCTION        
        self.number_of_hidden_layers = NUMBER_OF_HIDDEN_LAYERS
        self.number_of_neurons_in_first_hidden_layer = 8
        self.number_of_neurons_in_other_hidden_layers = 6
        self.verbose = VERBOSE
        self._accuracy = 0

    @property
    def epoch_number(self):
        return self._epoch_number

    @epoch_number.setter
    def epoch_number(self, value):
        self._epoch_number = value

    @property
    def batch_size_number(self):
        return self._batch_size_number

    @batch_size_number.setter
    def batch_size_number(self, value):
        self._batch_size_number = value
    
    @property
    def cost_function(self):
        return self._cost_function

    @cost_function.setter
    def cost_function(self, value):
        self._cost_function = value

    @property
    def optimizer(self):
        return self._optimizer

    @optimizer.setter
    def optimizer(self, value):
        self._optimizer = value

    @property
    def kernel_initializer(self):
        return self._kernel_initializer

    @kernel_initializer.setter
    def kernel_initializer(self, value):
        self._kernel_initializer = value

    @property
    def activation_function(self):
        return self._activation_function

    @activation_function.setter
    def activation_function(self, value):
        self._activation_function = value

    @property
    def number_of_hidden_layers(self):
        return self._number_of_hidden_layers

    @number_of_hidden_layers.setter
    def number_of_hidden_layers(self, value):
        self._number_of_hidden_layers = value

    @property
    def number_of_neurons_in_first_hidden_layer(self):
        return self._number_of_neurons_in_first_hidden_layer

    @number_of_neurons_in_first_hidden_layer.setter
    def number_of_neurons_in_first_hidden_layer(self, value):
        self._number_of_neurons_in_first_hidden_layer = value

    @property
    def number_of_neurons_in_other_hidden_layers(self):
        return self._number_of_neurons_in_other_hidden_layers

    @number_of_neurons_in_other_hidden_layers.setter
    def number_of_neurons_in_other_hidden_layers(self, value):
        self._number_of_neurons_in_other_hidden_layers = value

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value