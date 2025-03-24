import { Library, Book } from '../../library_manager';

export default function handler(req, res) {
  const lib = new Library();
  
  if (req.method === 'GET') {
    res.status(200).json(lib.books);
  } 
  else if (req.method === 'POST') {
    const book = new Book(...Object.values(req.body));
    lib.add_book(book);
    res.status(201).json({ status: 'success' });
  }
}
