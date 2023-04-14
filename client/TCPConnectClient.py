if __name__ == '__main__':
    cf = EchoClientFactory()
    chat_from = sys.argv[1]
    all_phone_numbers = ['000001', '000002', '000003', '000004']
    all_phone_numbers.remove(chat_from)
    import random
    reactor.callLater(3, cf.p.send_verify, chat_from)
    reactor.callLater(10, cf.p.send_single_chat, chat_from, random.choice(all_phone_numbers), '你好,这是单聊')
    reactor.callLater(10, cf.p.send_single_chat, chat_from, random.choice(all_phone_numbers), '你好,这是单聊')
    # reactor.callLater(11, cf.p.send_group_chat, chat_from, [random.choice(all_phone_numbers), random.choice(all_phone_numbers)], '你好,这是组聊')
    # reactor.callLater(12, cf.p.send_broadcast_chat, chat_from, '你好,这是群聊')

    reactor.connectTCP('127.0.0.1', 8124, cf)

    reactor.run()