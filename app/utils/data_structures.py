class Stack:
    """
    Implementación de una pila (LIFO) 
    """
    def __init__(self, max_size=100):
        self.items = []
        self.max_size = max_size
    
    def push(self, item):
        """Añade un elemento a la pila"""
        if len(self.items) >= self.max_size:
            self.items.pop(0)  # Elimina el elemento más antiguo si se alcanza el tamaño máximo
        self.items.append(item)
    
    def pop(self):
        """Elimina y devuelve el elemento superior de la pila"""
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def peek(self):
        """Devuelve el elemento superior sin eliminarlo"""
        if not self.is_empty():
            return self.items[-1]
        return None
    
    def is_empty(self):
        """Verifica si la pila está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Devuelve el tamaño de la pila"""
        return len(self.items)
    
    def clear(self):
        """Vacía la pila"""
        self.items = []


class Queue:
    """
    Implementación de una cola (FIFO) para procesamiento secuencial de acciones.
    """
    def __init__(self):
        self.items = []
    
    def enqueue(self, item):
        """Añade un elemento al final de la cola"""
        self.items.append(item)
    
    def dequeue(self):
        """Elimina y devuelve el primer elemento de la cola"""
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def peek(self):
        """Devuelve el primer elemento sin eliminarlo"""
        if not self.is_empty():
            return self.items[0]
        return None
    
    def is_empty(self):
        """Verifica si la cola está vacía"""
        return len(self.items) == 0
    
    def size(self):
        """Devuelve el tamaño de la cola"""
        return len(self.items)
    
    def clear(self):
        """Vacía la cola"""
        self.items = []


class DynamicArray:
    """
    Implementación de un arreglo dinámico para almacenamiento flexible de datos.
    """
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.array = [None] * capacity
    
    def append(self, item):
        """Añade un elemento al final del arreglo"""
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        self.array[self.size] = item
        self.size += 1
    
    def insert(self, index, item):
        """Inserta un elemento en una posición específica"""
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")
        
        if self.size == self.capacity:
            self._resize(2 * self.capacity)
        
        # Desplazar elementos a la derecha
        for i in range(self.size, index, -1):
            self.array[i] = self.array[i-1]
        
        self.array[index] = item
        self.size += 1
    
    def remove(self, item):
        """Elimina la primera ocurrencia de un elemento"""
        for i in range(self.size):
            if self.array[i] == item:
                self._remove_at(i)
                return True
        return False
    
    def _remove_at(self, index):
        """Elimina un elemento en una posición específica"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        
        # Desplazar elementos a la izquierda
        for i in range(index, self.size - 1):
            self.array[i] = self.array[i+1]
        
        self.array[self.size - 1] = None
        self.size -= 1
        
        # Reducir el tamaño del arreglo si es necesario
        if self.size > 0 and self.size == self.capacity // 4:
            self._resize(self.capacity // 2)
    
    def _resize(self, new_capacity):
        """Redimensiona el arreglo interno"""
        new_array = [None] * new_capacity
        for i in range(self.size):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity
    
    def get(self, index):
        """Obtiene el elemento en una posición específica"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        return self.array[index]
    
    def set(self, index, item):
        """Establece el valor de un elemento en una posición específica"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")
        self.array[index] = item
    
    def __len__(self):
        """Devuelve el tamaño del arreglo"""
        return self.size
    
    def __getitem__(self, index):
        """Permite acceder a los elementos con la sintaxis de corchetes"""
        return self.get(index)
    
    def __setitem__(self, index, item):
        """Permite establecer elementos con la sintaxis de corchetes"""
        self.set(index, item)
    
    def __iter__(self):
        """Permite iterar sobre el arreglo"""
        for i in range(self.size):
            yield self.array[i]


class ActionHistory:
    """
    Clase para gestionar el historial de acciones con capacidad de deshacer/rehacer.
    Utiliza dos pilas: una para deshacer y otra para rehacer.
    """
    def __init__(self, max_size=50):
        self.undo_stack = Stack(max_size)
        self.redo_stack = Stack(max_size)
    
    def add_action(self, action):
        """
        Añade una acción al historial.
        Una acción debe ser un diccionario con al menos:
        - 'type': tipo de acción
        - 'data': datos de la acción
        - 'undo_function': función para deshacer la acción
        - 'redo_function': función para rehacer la acción
        """
        self.undo_stack.push(action)
        self.redo_stack.clear()  # Al añadir una nueva acción, se borra el historial de rehacer
    
    def undo(self):
        """Deshace la última acción"""
        if not self.undo_stack.is_empty():
            action = self.undo_stack.pop()
            if 'undo_function' in action and callable(action['undo_function']):
                action['undo_function'](action['data'])
            self.redo_stack.push(action)
            return action
        return None
    
    def redo(self):
        """Rehace la última acción deshecha"""
        if not self.redo_stack.is_empty():
            action = self.redo_stack.pop()
            if 'redo_function' in action and callable(action['redo_function']):
                action['redo_function'](action['data'])
            self.undo_stack.push(action)
            return action
        return None
    
    def can_undo(self):
        """Verifica si hay acciones para deshacer"""
        return not self.undo_stack.is_empty()
    
    def can_redo(self):
        """Verifica si hay acciones para rehacer"""
        return not self.redo_stack.is_empty()
    
    def clear(self):
        """Limpia todo el historial"""
        self.undo_stack.clear()
        self.redo_stack.clear()


class ActionQueue:
    """
    Clase para procesar acciones de forma secuencial.
    Utiliza una cola para almacenar las acciones pendientes.
    """
    def __init__(self):
        self.queue = Queue()
        self.processing = False
    
    def add_action(self, action):
        """
        Añade una acción a la cola.
        Una acción debe ser un diccionario con al menos:
        - 'type': tipo de acción
        - 'data': datos de la acción
        - 'process_function': función para procesar la acción
        """
        self.queue.enqueue(action)
    
    def process_next(self):
        """Procesa la siguiente acción en la cola"""
        if not self.queue.is_empty() and not self.processing:
            self.processing = True
            action = self.queue.dequeue()
            if 'process_function' in action and callable(action['process_function']):
                result = action['process_function'](action['data'])
            else:
                result = None
            self.processing = False
            return result
        return None
    
    def process_all(self):
        """Procesa todas las acciones en la cola"""
        results = []
        while not self.queue.is_empty():
            result = self.process_next()
            if result is not None:
                results.append(result)
        return results
    
    def is_empty(self):
        """Verifica si la cola está vacía"""
        return self.queue.is_empty()
    
    def size(self):
        """Devuelve el tamaño de la cola"""
        return self.queue.size()
    
    def clear(self):
        """Vacía la cola"""
        self.queue.clear()
