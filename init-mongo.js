db = connect("mongodb://localhost:27017/it");

var initialData = [
    {
        link: "http://example.com",
        name: "Tom",
        username: "No. 189, Grove St, Los Angeles",
        password: "aaaaaaaaaaa",
    },
    {
        link: "http://example.com",
        name: "Jerry",
        username: "No. 123, Elm St, New York",
        password: "123456",
    }
];

var initialEvent = [
    {
        date: "2024-01-01",
        title: "Test",
        question: "Test",
        description: "Test",
        answer: "Test"
    },
    {
        date: "2024-01-01",
        title: "Test",
        question: "Test",
        description: "Test",
        answer: "Test"
    }
]

db.link_list.insertMany(initialData);
db.event.insertMany(initialEvent);

db.users.insertMany([
    {
        username: 'admin_user',
        password: '$2b$10$VDYowU8aAQdOR3Dz1xEoVOF9QJWdStymturxGMdKRRMfFrxQrkAa6',
        role: 'admin',
        created_at: new Date()
    }
]);

print("Initial data inserted successfully");
