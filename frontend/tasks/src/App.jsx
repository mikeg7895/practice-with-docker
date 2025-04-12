// App.jsx
import { useEffect, useState } from 'react';
import axios from 'axios';

const API_URL = 'http://18.218.42.4:8000/tasks';

function App() {
  const [tasks, setTasks] = useState([]);
  const [newTask, setNewTask] = useState({ id: '', title: '', description: '', completed: false });

  useEffect(() => {
    axios.get(API_URL).then(res => setTasks(res.data));
  }, []);

  const handleCreate = () => {
    axios.post(API_URL, newTask).then(res => {
      setTasks([...tasks, res.data]);
      setNewTask({ id: '', title: '', description: '', completed: false });
    });
  };

  const handleDelete = (id) => {
    axios.delete(`${API_URL}/${id}`).then(() => {
      setTasks(tasks.filter(task => task.id !== id));
    });
  };

  const handleToggle = (task) => {
    const updated = { ...task, completed: !task.completed };
    axios.put(`${API_URL}/${task.id}`, updated).then(res => {
      setTasks(tasks.map(t => (t.id === task.id ? res.data : t)));
    });
  };

  return (
    <div className="p-4">
      <h1 className="text-xl font-bold">Task Manager</h1>
      <input placeholder="ID" value={newTask.id} onChange={e => setNewTask({ ...newTask, id: Number(e.target.value) })} />
      <input placeholder="Title" value={newTask.title} onChange={e => setNewTask({ ...newTask, title: e.target.value })} />
      <input placeholder="Description" value={newTask.description} onChange={e => setNewTask({ ...newTask, description: e.target.value })} />
      <button onClick={handleCreate}>Add Task</button>
      <ul>
        {tasks.map(task => (
          <li key={task.id} className="mt-2">
            <span
              onClick={() => handleToggle(task)}
              style={{ textDecoration: task.completed ? 'line-through' : 'none', cursor: 'pointer' }}
            >
              {task.title}: {task.description}
            </span>
            <button onClick={() => handleDelete(task.id)} className="ml-2 text-red-500">Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
