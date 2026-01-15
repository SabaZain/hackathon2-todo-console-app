const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-blue-800 to-indigo-900 text-white py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-sm opacity-90">
            © {currentYear} Todo App. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;