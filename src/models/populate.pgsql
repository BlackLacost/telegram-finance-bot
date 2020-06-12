INSERT INTO category (codename, name, is_base_expense, aliases)
VALUES
  ('products', 'продукты', true, 'еда'),
  ('coffee', 'кофе', true, ''),
  ('dinner', 'обед', true, 'столовая, ланч, бизнес-ланч, бизнес ланч'),
  ('cafe', 'кафе', true, 'ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio'),
  ('transport', 'общ. транспорт', false, 'метро, автобус, metro'),
  ('taxi', 'такси', false, 'яндекс такси, yandex taxi'),
  ('phone', 'телефон', false, 'теле2, связь'),
  ('books', 'книги', false, 'литература, литра, лит-ра'),
  ('internet', 'интернет', false, 'инет, inet'),
  ('subscriptions', 'подписки', false, 'подписка'),
  ('other', 'прочее', true, '');

INSERT INTO budget(codename, daily_limit)
VALUES ('base', 500);
