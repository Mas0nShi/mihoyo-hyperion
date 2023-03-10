import scheduler


def handler(event, context):
    scheduler.run()


if __name__ == '__main__':
    scheduler.run()
